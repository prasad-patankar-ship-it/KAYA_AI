import os
import json
import requests


# ============================================================
# KAYA AI BACKENDS
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen3:1.7b"

# Cloud mode is automatically detected on Streamlit Cloud.
# Set KAYA_CLOUD_MODE=true in Streamlit Secrets for cloud.
CLOUD_MODE = os.getenv("KAYA_CLOUD_MODE", "").lower() == "true"


# ============================================================
# LOCAL QWEN
# ============================================================

def ask_qwen(prompt):

    payload = {
        "model": OLLAMA_MODEL,
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


# ============================================================
# CLOUD GEMINI
# ============================================================

def ask_gemini_cloud(prompt):

    try:

        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        client = genai.Client(
            api_key=api_key
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        if response and response.text:
            return response.text.strip()

        raise ValueError(
            "Gemini returned an empty response."
        )

    except Exception as e:

        raise RuntimeError(
            f"Cloud AI error: {e}"
        )


# ============================================================
# UNIFIED AI FUNCTION
# ============================================================

def ask_ai(prompt):

    # --------------------------------------------------------
    # CLOUD
    # --------------------------------------------------------

    if CLOUD_MODE:

        return ask_gemini_cloud(prompt)

    # --------------------------------------------------------
    # LOCAL
    # --------------------------------------------------------

    return ask_qwen(prompt)


# ============================================================
# KAYA RESPONSE
# ============================================================

def ask_kaya_local(
    prompt,
    language="English"
):

    system_prompt = f"""
You are KAYA, a friendly multilingual
healthcare assistant.

Respond in {language}.

Keep responses concise, clear and easy
to understand.

You can help with:

- medication schedules
- general medicine information
- prescription organization
- reminders
- general health questions
- medical report understanding

Never invent:

- prescriptions
- dosages
- diagnoses
- medical records
- medical test results

Do not claim that a medicine has been taken
unless the application has recorded it as
completed.

For serious medical concerns, advise the user
to consult a qualified healthcare professional.

Always communicate safely and clearly.
"""

    full_prompt = (
        system_prompt
        + "\n\n"
        + "User:\n"
        + prompt
    )

    return ask_ai(full_prompt)


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(user_message):

    prompt = f"""
You are KAYA's medication command detector.

Classify the user's request.

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

        result = ask_ai(prompt)

        result = result.strip()

        # ----------------------------------------------------
        # Remove markdown JSON fences if model adds them
        # ----------------------------------------------------

        if result.startswith("```json"):

            result = result[
                len("```json"):
            ]

        if result.startswith("```"):

            result = result[
                len("```"):
            ]

        if result.endswith("```"):

            result = result[
                :-3
            ]

        result = result.strip()

        # ----------------------------------------------------
        # Extract JSON if model added extra text
        # ----------------------------------------------------

        start = result.find("{")
        end = result.rfind("}")

        if start != -1 and end != -1:

            result = result[
                start:end + 1
            ]

        data = json.loads(result)

        if not isinstance(data, dict):

            raise ValueError(
                "Invalid intent response"
            )

        # ----------------------------------------------------
        # Ensure required fields exist
        # ----------------------------------------------------

        data.setdefault(
            "intent",
            "GENERAL_QUESTION"
        )

        data.setdefault(
            "medicine_name",
            ""
        )

        data.setdefault(
            "time",
            ""
        )

        data.setdefault(
            "instructions",
            ""
        )

        data.setdefault(
            "frequency",
            "Daily"
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