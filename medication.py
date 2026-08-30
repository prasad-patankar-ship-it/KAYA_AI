import json
import os

MEDICATION_FILE = "medications.json"


def load_medications():

    if not os.path.exists(MEDICATION_FILE):
        return []

    try:
        with open(
            MEDICATION_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_medications(medications):

    with open(
        MEDICATION_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            medications,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_medication(
    name,
    time,
    instructions="",
    frequency="Daily"
):

    medications = load_medications()

    medications.append({
        "name": name,
        "time": time,
        "instructions": instructions,
        "frequency": frequency,
        "status": "Upcoming"
    })

    save_medications(medications)


def delete_medication(index):

    medications = load_medications()

    if 0 <= index < len(medications):

        medications.pop(index)

        save_medications(medications)


def update_medication_status(
    index,
    status
):

    medications = load_medications()

    if 0 <= index < len(medications):

        medications[index]["status"] = status

        save_medications(medications)