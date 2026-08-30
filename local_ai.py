import requests
import json


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:1.7b"


def ask_qwen(prompt):

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"].strip()


def ask_kaya_local(
    prompt,
    language="English"
):

    system_prompt = f"""
You are KAYA, a friendly multilingual
healthcare assistant.

Respond in {language}.

Keep responses concise and easy to understand.

You can help with:
- medication schedules
- general medicine information
- prescription organization
- reminders
- general health questions

Never invent prescriptions, dosages,
diagnoses, or medical records.

Do not claim that a medicine has been taken
unless the application has recorded it as
completed.

For serious medical concerns, advise the user
to consult a qualified healthcare professional.
"""

    return ask_qwen(
        system_prompt
        + "\n\n"
        + prompt
    )


def detect_intent(user_message):

    prompt = f"""
You are KAYA's local intent detector.

Classify this user request.

Return ONLY valid JSON.
Do not write anything before or after the JSON.

Possible intents:

ADD_MEDICINE
DELETE_MEDICINE
COMPLETE_MEDICINE
SHOW_MEDICINES
CHECK_DUE_MEDICINE
GENERAL_QUESTION

User message:
{user_message}

Return exactly this structure:

{{
    "intent": "GENERAL_QUESTION",
    "medicine_name": "",
    "time": "",
    "instructions": "",
    "frequency": "Daily"
}}
"""

    try:

        result = ask_qwen(prompt)

        result = result.strip()

        if "```json" in result:

            result = result.replace(
                "```json",
                ""
            )

        if "```" in result:

            result = result.replace(
                "```",
                ""
            )

        result = result.strip()

        data = json.loads(result)

        if not isinstance(data, dict):

            raise ValueError(
                "Invalid intent response"
            )

        return data

    except Exception as e:

        print(
            f"Intent detection error: {e}"
        )

        return {
            "intent": "GENERAL_QUESTION",
            "medicine_name": "",
            "time": "",
            "instructions": "",
            "frequency": "Daily"
        }