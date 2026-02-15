import json
import logging
import os
from json import JSONDecodeError
import random

from src.ugh_no.model.ugh_enums import ToneEnum, StyleEnum, SeverityEnum, LengthEnum
from src.ugh_no.model.ugh_model import UghNoResponse

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH_RULE_JSON = os.path.join(BASE_DIR, "..", "..", "resources", "rules_based", "rules-based-updated.json")
MODEL_PATH_RULE_JSON = os.path.normpath(MODEL_PATH_RULE_JSON)

def load_rules_based_file() -> UghNoResponse | None:
    try:
        with open(MODEL_PATH_RULE_JSON, "r") as rule_json_file:
            rules_json = rule_json_file.read()
            rules_json_read = json.loads(rules_json)
            logger.info("Loaded rules-based JSON file successfully.")
            if "rules_responses" in rules_json_read:
                #print(rules_json_read)
                #print(rules_json_read['rules_responses'])
                array_responses = rules_json_read['rules_responses']
                filtered_data = [response for response in array_responses if response["tone"] == "polite" and response["severity_level"] == "low"]
                logger.info("Found matching response:", filtered_data)

                if len(filtered_data) > 0:
                    random_chosen = random.choice(filtered_data)
                    response_obj = UghNoResponse(**random_chosen)
                    logger.info(f"Deserialized json to Python object {response_obj}")
                    return response_obj

                return UghNoResponse(tone=ToneEnum.neutral, humour_level=5, directness=5, length=LengthEnum.short, style= StyleEnum.professional, severity_level=SeverityEnum.low, response="Based Response not matched with criteria.")

    except FileNotFoundError as e:
        logger.error(f" Function load_rules_based_file -> File not found!: {str(e)}")
    except JSONDecodeError as e:
        logger.error(f"Invalid JSON format!: {str(e)}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

