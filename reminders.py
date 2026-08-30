from datetime import datetime
from medication import load_medications


def get_due_reminders():

    medications = load_medications()

    current_time = datetime.now().strftime("%H:%M")

    reminders = []

    for medicine in medications:

        if medicine.get("status", "Upcoming") == "Completed":
            continue

        medicine_time = medicine.get("time", "")

        if medicine_time == current_time:

            reminders.append({
                "name": medicine.get(
                    "name",
                    "Medicine"
                ),
                "time": medicine_time,
                "instructions": medicine.get(
                    "instructions",
                    ""
                )
            })

    return reminders


def get_upcoming_reminders():

    medications = load_medications()

    current_time = datetime.now().strftime("%H:%M")

    reminders = []

    for medicine in medications:

        if medicine.get("status", "Upcoming") == "Completed":
            continue

        medicine_time = medicine.get("time", "")

        if medicine_time > current_time:

            reminders.append({
                "name": medicine.get(
                    "name",
                    "Medicine"
                ),
                "time": medicine_time,
                "instructions": medicine.get(
                    "instructions",
                    ""
                )
            })

    return sorted(
        reminders,
        key=lambda x: x["time"]
    )


def reminder_message(language="English"):

    medicines = get_due_reminders()

    if not medicines:
        return None

    names = [
        medicine["name"]
        for medicine in medicines
    ]

    if language == "हिन्दी":

        return (
            "💊 दवाई लेने का समय है: "
            + ", ".join(names)
        )

    if language == "मराठी":

        return (
            "💊 औषध घेण्याची वेळ झाली आहे: "
            + ", ".join(names)
        )

    return (
        "💊 It is time to take: "
        + ", ".join(names)
    )