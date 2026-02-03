import os
import logging
import openai
from json import JSONDecodeError
from fastapi import FastAPI, HTTPException, status
from openai import OpenAI
from fastapi_versionizer.versionizer import Versionizer, api_version

from src.ugh_no.endpoint.errors.constants import functional_errors
from src.ugh_no.endpoint.errors.custom_exception import UserException
from src.ugh_no.endpoint.logic import file_rules_from_json
from src.ugh_no.model.ugh_model import UghNoRequest, UghNoResponse

# Get the folder where the current script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Go to the model folder relative to this file
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

        print(content)
        print(system_prompt)
except FileNotFoundError as e:
    print(f"File not found!: {str(e)}")
except JSONDecodeError as e:
    print(f"Invalid JSON format!: {str(e)}")
except Exception as e:
    print(f"An error occurred: {str(e)}")

app = FastAPI(title="Ugh No Endpoint", version="1.0.0")


@api_version(1)
@app.post("/generate-response", response_model=UghNoResponse)
async def generate_response(request: UghNoRequest):
    # format the loaded `content` string using request attributes (placeholders like {name} in `user_prompt.txt`)
    logging.info("Request received with headers: ", request.dict())
    user_prompt = content.format(**request.dict())

    if request.instant_mode:
        logging.info("Instant mode enabled, using fallback response.")
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
        print("Rate limit error:", e)
        logging.error("Rate limit error ", e)
        # HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(e))
        raise UserException(functional_errors.C_TF_0001_RATE_LIMIT_ERROR)
    except openai.error.AuthenticationError as e:
        print("Authentication error:", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except openai.error.APIConnectionError as e:
        print("Connection error:", e)
        logging.error(HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)
    except openai.error.Timeout as e:
        print("Timeout error:", e)
        logging.error(HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e)))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)
    except openai.error.APIError as e:
        print("API error:", e)
        logging.error(HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e)))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)
    except Exception as e:
        logging.error("Unexpected error calling OpenAI:", e)
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)

    # Validate response structure
    if not completion or not getattr(completion, "choices", None):
        logging.error("Invalid response from OpenAI:", completion)
        logging.error(HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Invalid response from OpenAI"))
        raise UserException(functional_errors.C_TF_0002_GENERAL_API_ERROR)

    print("OpenAI response: ", completion)
    response = UghNoResponse(response_text=completion.choices[0].message.content.strip())
    print("Generated response: ", response)
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
    json_response_random = file_rules_from_json.load_rules_based_file()
    if json_response_random is None:
        return create_response_object(request, "I'm sorry, but I couldn't generate a response at this time.")
    else:
        return create_response_object(request, json_response_random.response)


versions = Versionizer(app,
                       prefix_format="v{major}",
                       semantic_version_format="{major}",
                       latest_prefix="latest",
                       sort_routes=True
                       ).versionize()