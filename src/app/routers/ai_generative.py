import os
import logging
import openai
from json import JSONDecodeError
from fastapi import APIRouter, HTTPException, status
from openai import OpenAI
from fastapi_versionizer.versionizer import Versionizer

from errors.constants import functional_errors
from errors.custom_exception import UserException
from app.routers.utility import load_rules_from_json
from app.schemas.ugh_model import UghNoRequest, UghNoResponse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the folder where the current script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go to the schemas folder relative to this file
MODEL_PATH_USER_PROMPT = os.path.join(BASE_DIR, "..", "resources", "user_prompt.txt")
MODEL_PATH_SYSTEM_PROMPT = os.path.join(BASE_DIR, "..", "resources", "system_prompt.txt")
# Normalize the path for Linux
MODEL_PATH_USER_PROMPT = os.path.normpath(MODEL_PATH_USER_PROMPT)
MODEL_PATH_SYSTEM_PROMPT = os.path.normpath(MODEL_PATH_SYSTEM_PROMPT)

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError("Environment variable `OPENAI_API_KEY` is not set")
client = OpenAI(api_key=api_key)

try:
    with (open(MODEL_PATH_USER_PROMPT, "r") as user_prompt_file, open(MODEL_PATH_SYSTEM_PROMPT,
                                                                      "r") as system_prompt_file):
        content = user_prompt_file.read()
        system_prompt = system_prompt_file.read()

        logger.debug(content)
        logger.debug(system_prompt)
except FileNotFoundError as e:
    logger.error(f"File not found!: {str(e)}")
except JSONDecodeError as e:
    logger.error(f"Invalid JSON format!: {str(e)}")
except Exception as e:
    logger.error(f"An error occurred: {str(e)}")

router = APIRouter(tags=["AI Generative"])


#@api_version(1)
@router.post("/generate-response", response_model=UghNoResponse)
async def generate_response(request: UghNoRequest):
    # format the loaded `content` string using request attributes (placeholders like {name} in `user_prompt.txt`)
    logger.info("Request received with headers: ", request.dict())
    user_prompt = content.format(**request.dict())

    if request.instant_mode:
        logger.info("Instant mode enabled, using fallback response.")
        return fallback_generate_response(request)

    try:
        # Call OpenAI API
        # UPDATE gpt-4.1-mini TO gpt-4o-mini because of price
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=60,
        )

    except openai.error.RateLimitError as e:
        logger.error("Rate limit error ", e)
        # HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))
        raise UserException(functional_errors.C_TF_0001_RATE_LIMIT_ERROR)
    except openai.error.AuthenticationError as e:
        logger.error("Authentication error:", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except openai.error.APIConnectionError as e:
        print("Connection error:", e)
        logger.error(HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)
    except openai.error.Timeout as e:
        print("Timeout error:", e)
        logger.error(HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e)))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)
    except openai.error.APIError as e:
        print("API error:", e)
        logger.error(HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e)))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)
    except Exception as e:
        logger.error("Unexpected error calling OpenAI:", e)
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)

    # Validate response structure
    if not completion or not getattr(completion, "choices", None):
        logger.error("Invalid response from OpenAI:", completion)
        logger.error(HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid response from OpenAI"))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)

    logger.debug("OpenAI response: ", completion)
    response = UghNoResponse(response_text=completion.choices[0].message.content.strip())
    logger.debug("Generated response: ", response)
    return response


def create_response_object(request: UghNoRequest, response_text: str) -> UghNoResponse:
    return UghNoResponse(
        tone=request.tone,
        humour_level=request.humour_level,
        directness=request.directness,
        length=request.length,
        style=request.style,
        severity_level=request.severity_level,
        response=response_text
    )


def fallback_generate_response(request: UghNoRequest) -> UghNoResponse:
    # Simple fallback logic
    json_response_random = load_rules_from_json.load_rules_based_file()
    if json_response_random is None:
        return create_response_object(request, "I'm sorry, but I couldn't generate a response at this time.")
    else:
        return create_response_object(request, json_response_random.response)
