from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from local_ai import ask_kaya_local, detect_intent

from medication import (
    add_medication,
    load_medications,
    delete_medication,
    update_medication_status
)

from reminders import reminder_message


# ==========================================
# KAYA API SERVER
# ==========================================

app = FastAPI(
    title="KAYA AI API",
    version="1.0"
)


# ==========================================
# ANDROID CONNECTION
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==========================================
# REQUEST MODELS
# ==========================================

class ChatRequest(BaseModel):

    message: str
    language: str = "English"


class MedicationRequest(BaseModel):

    name: str
    time: str
    instructions: str = ""
    frequency: str = "Daily"


class StatusRequest(BaseModel):

    status: str = "Completed"


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "name": "KAYA AI",
        "status": "online",
        "ai": "Qwen3 1.7B",
        "version": "1.0"
    }


# ==========================================
# CHAT
# ==========================================

@app.post("/chat")
def chat(request: ChatRequest):

    message = request.message.strip()

    if not message:

        return {
            "response": "Please tell me how I can help you."
        }

    try:

        intent_data = detect_intent(message)

        intent = intent_data.get(
            "intent",
            "GENERAL_QUESTION"
        )

        # --------------------------------------
        # SHOW MEDICINES
        # --------------------------------------

        if intent == "SHOW_MEDICINES":

            medications = load_medications()

            if not medications:

                return {
                    "response": (
                        "You don't have any medicines "
                        "saved yet."
                    ),
                    "intent": intent,
                    "medications": []
                }

            medicine_text = []

            for medicine in medications:

                medicine_text.append(
                    f"{medicine.get('name', 'Medicine')} "
                    f"at {medicine.get('time', '')}"
                )

            return {
                "response": (
                    "Your saved medicines are: "
                    + ", ".join(medicine_text)
                ),
                "intent": intent,
                "medications": medications
            }

        # --------------------------------------
        # GENERAL AI
        # --------------------------------------

        response = ask_kaya_local(
            message,
            request.language
        )

        return {
            "response": response,
            "intent": intent
        }

    except Exception as e:

        return {
            "response": "KAYA could not process your request.",
            "error": str(e)
        }


# ==========================================
# GET ALL MEDICATIONS
# ==========================================

@app.get("/medications")
def get_medications():

    return {
        "medications": load_medications()
    }


# ==========================================
# ADD MEDICATION
# ==========================================

@app.post("/medications")
def create_medication(
    request: MedicationRequest
):

    try:

        add_medication(
            request.name,
            request.time,
            request.instructions,
            request.frequency
        )

        return {
            "success": True,
            "message": "Medicine added successfully.",
            "medications": load_medications()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ==========================================
# DELETE MEDICATION
# ==========================================

@app.delete("/medications/{index}")
def remove_medication(index: int):

    try:

        medications = load_medications()

        if index < 0 or index >= len(medications):

            return {
                "success": False,
                "message": "Medicine not found."
            }

        delete_medication(index)

        return {
            "success": True,
            "message": "Medicine deleted successfully.",
            "medications": load_medications()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ==========================================
# COMPLETE MEDICATION
# ==========================================

@app.put("/medications/{index}/status")
def complete_medication(
    index: int,
    request: StatusRequest
):

    try:

        medications = load_medications()

        if index < 0 or index >= len(medications):

            return {
                "success": False,
                "message": "Medicine not found."
            }

        update_medication_status(
            index,
            request.status
        )

        return {
            "success": True,
            "message": "Medicine status updated.",
            "medications": load_medications()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ==========================================
# REMINDER
# ==========================================

@app.get("/reminder")
def reminder(
    language: str = "English"
):

    message = reminder_message(
        language
    )

    return {
        "reminder": message
    }
    