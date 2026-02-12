>[!IMPORTANT]
>Development still in process

# ughno-bd
This project is a lightweight API service built with Python and FastAPI that generates structured responses to unsolicited images using the OpenAI API.

The system is designed to:

* Analyze incoming user messages
* Classify content severity (e.g., boundary, warning, violation)
* Generate appropriate, policy-aligned responses
* Apply tone presets and rule-based fallbacks
* Return structured JSON outputs for easy frontend integration

The architecture combines:
* Rule-based validation for fast, low-cost filtering
* AI-powered response generation for nuanced cases
* Configurable tone, style, and escalation levels

## Tech Stack
- Python
- FastApi
- OpenAPI

