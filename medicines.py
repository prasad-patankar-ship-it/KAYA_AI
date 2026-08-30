from datetime import datetime

from medication import (
    load_medications,
    add_medication,
    delete_medication,
    update_medication_status
)


# ==========================================
# SHOW ALL MEDICATIONS
# ==========================================

def get_all_medications(language="English"):

    medications = load_medications()

    if not medications:

        messages = {
            "English": "You currently have no medicines saved.",
            "हिन्दी": "आपकी कोई दवाई अभी सेव नहीं है।",
            "मराठी": "तुमची कोणतीही औषधे सध्या सेव्ह केलेली नाहीत."
        }

        return messages.get(
            language,
            messages["English"]
        )

    result = []

    for medicine in medications:

        name = medicine.get(
            "name",
            "Unknown"
        )

        time = medicine.get(
            "time",
            "--:--"
        )

        frequency = medicine.get(
            "frequency",
            "Daily"
        )

        if language == "हिन्दी":

            result.append(
                f"{name} - समय {time} "
                f"({frequency})"
            )

        elif language == "मराठी":

            result.append(
                f"{name} - वेळ {time} "
                f"({frequency})"
            )

        else:

            result.append(
                f"{name} at {time} "
                f"({frequency})"
            )

    if language == "हिन्दी":

        return "आपकी दवाइयाँ:\n" + "\n".join(result)

    if language == "मराठी":

        return "तुमची औषधे:\n" + "\n".join(result)

    return "Your medicines:\n" + "\n".join(result)


# ==========================================
# CHECK DUE MEDICATION
# ==========================================

def get_medication_status(language="English"):

    medications = load_medications()

    if not medications:

        return get_all_medications(language)

    current_time = datetime.now().strftime(
        "%H:%M"
    )

    due_now = []
    upcoming = []
    completed = []

    for medicine in medications:

        name = medicine.get(
            "name",
            "Medicine"
        )

        time = medicine.get(
            "time",
            "--:--"
        )

        status = medicine.get(
            "status",
            "Upcoming"
        )

        if status == "Completed":

            completed.append(
                f"{name} at {time}"
            )

        elif time == current_time:

            due_now.append(
                f"{name} at {time}"
            )

        else:

            upcoming.append(
                f"{name} at {time}"
            )

    response = []

    if due_now:

        response.append(
            "Due now: " + ", ".join(due_now)
        )

    if upcoming:

        response.append(
            "Upcoming: " + ", ".join(upcoming)
        )

    if completed:

        response.append(
            "Completed: " + ", ".join(completed)
        )

    if not response:

        if language == "हिन्दी":
            return "अभी कोई दवाई निर्धारित नहीं है।"

        if language == "मराठी":
            return "सध्या कोणतीही औषधे निर्धारित नाहीत."

        return "No medication is due right now."

    result = "\n".join(response)

    # Basic language labels
    if language == "हिन्दी":

        result = result.replace(
            "Due now:",
            "अभी लेने वाली दवाई:"
        )

        result = result.replace(
            "Upcoming:",
            "आने वाली दवाइयाँ:"
        )

        result = result.replace(
            "Completed:",
            "पूरी की गई दवाइयाँ:"
        )

    elif language == "मराठी":

        result = result.replace(
            "Due now:",
            "आता घ्यायची औषधे:"
        )

        result = result.replace(
            "Upcoming:",
            "आगामी औषधे:"
        )

        result = result.replace(
            "Completed:",
            "पूर्ण केलेली औषधे:"
        )

    return result


# ==========================================
# MEDICATION QUESTION DETECTION
# ==========================================

def process_medication_question(
    message,
    language="English"
):

    text = message.lower().strip()

    # ------------------------------------------
    # ENGLISH
    # ------------------------------------------

    english_list = [
        "what medicines",
        "which medicines",
        "my medicines",
        "show medicines",
        "list medicines",
        "medicine list",
        "what medicine do i have",
        "which medicine do i have"
    ]

    english_due = [
        "due now",
        "medicine is due",
        "medicines are due",
        "what should i take",
        "what medicine should i take"
    ]

    # ------------------------------------------
    # HINDI
    # ------------------------------------------

    hindi_list = [
        "मेरी दवाइयां",
        "मेरी दवाइयाँ",
        "कौन सी दवाइयां",
        "कौन सी दवाइयाँ",
        "मेरी दवा कौन सी",
        "दवाइयों की सूची"
    ]

    hindi_due = [
        "अभी कौन सी दवाई",
        "कौन सी दवाई लेनी है",
        "कौन सी दवा लेनी है",
        "दवाई कब लेनी है",
        "दवा कब लेनी है"
    ]

    # ------------------------------------------
    # MARATHI
    # ------------------------------------------

    marathi_list = [
        "माझी औषधे",
        "माझी औषधं",
        "कोणती औषधे",
        "कोणती औषधं",
        "माझी औषधे कोणती",
        "औषधांची यादी"
    ]

    marathi_due = [
        "आता कोणते औषध",
        "कोणते औषध घ्यायचे",
        "औषध कधी घ्यायचे",
        "आता कोणती औषधे"
    ]

    # ------------------------------------------
    # CHECK LIST
    # ------------------------------------------

    for phrase in english_list:

        if phrase in text:

            return get_all_medications(
                language
            )

    for phrase in hindi_list:

        if phrase in text:

            return get_all_medications(
                "हिन्दी"
            )

    for phrase in marathi_list:

        if phrase in text:

            return get_all_medications(
                "मराठी"
            )

    # ------------------------------------------
    # CHECK DUE
    # ------------------------------------------

    for phrase in english_due:

        if phrase in text:

            return get_medication_status(
                language
            )

    for phrase in hindi_due:

        if phrase in text:

            return get_medication_status(
                "हिन्दी"
            )

    for phrase in marathi_due:

        if phrase in text:

            return get_medication_status(
                "मराठी"
            )

    return None


# ==========================================
# ADD MEDICINE
# ==========================================

def add_medicine_action(
    name,
    time,
    instructions="",
    frequency="Daily",
    language="English"
):

    add_medication(
        name,
        time,
        instructions,
        frequency
    )

    if language == "हिन्दी":

        return (
            f"✅ {name} को {time} बजे "
            "आपकी दवाई की सूची में जोड़ दिया गया है।"
        )

    if language == "मराठी":

        return (
            f"✅ {name} हे औषध {time} वाजता "
            "तुमच्या औषधांच्या यादीत जोडले आहे."
        )

    return (
        f"✅ {name} has been added to "
        f"your medication schedule at {time}."
    )


# ==========================================
# DELETE MEDICINE
# ==========================================

def delete_medicine_action(
    name,
    language="English"
):

    medications = load_medications()

    for index, medicine in enumerate(medications):

        if medicine.get(
            "name",
            ""
        ).lower() == name.lower():

            delete_medication(index)

            if language == "हिन्दी":

                return (
                    f"✅ {name} को आपकी "
                    "दवाई की सूची से हटा दिया गया है।"
                )

            if language == "मराठी":

                return (
                    f"✅ {name} हे औषध "
                    "तुमच्या यादीतून काढले आहे."
                )

            return (
                f"✅ {name} has been removed "
                f"from your medication list."
            )

    if language == "हिन्दी":

        return f"मुझे {name} आपकी दवाई की सूची में नहीं मिली।"

    if language == "मराठी":

        return f"मला {name} तुमच्या औषधांच्या यादीत सापडले नाही."

    return (
        f"I couldn't find {name} "
        f"in your medication list."
    )


# ==========================================
# COMPLETE MEDICINE
# ==========================================

def complete_medicine_action(
    name,
    language="English"
):

    medications = load_medications()

    for index, medicine in enumerate(medications):

        if medicine.get(
            "name",
            ""
        ).lower() == name.lower():

            update_medication_status(
                index,
                "Completed"
            )

            if language == "हिन्दी":

                return (
                    f"✅ {name} को पूरा किया हुआ "
                    "मार्क कर दिया गया है।"
                )

            if language == "मराठी":

                return (
                    f"✅ {name} हे औषध पूर्ण "
                    "केलेले म्हणून मार्क केले आहे."
                )

            return (
                f"✅ {name} has been marked "
                f"as completed."
            )

    if language == "हिन्दी":

        return f"मुझे {name} आपकी दवाई की सूची में नहीं मिली।"

    if language == "मराठी":

        return f"मला {name} तुमच्या औषधांच्या यादीत सापडले नाही."

    return (
        f"I couldn't find {name} "
        f"in your medication list."
    )