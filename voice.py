import speech_recognition as sr


def listen(language="English"):

    recognizer = sr.Recognizer()

    language_codes = {
        "English": "en-IN",
        "हिन्दी": "hi-IN",
        "मराठी": "mr-IN"
    }

    recognition_language = language_codes.get(
        language,
        "en-IN"
    )

    try:

        with sr.Microphone() as source:

            print("KAYA is listening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=15
            )

        text = recognizer.recognize_google(
            audio,
            language=recognition_language
        )

        print(
            f"You said: {text}"
        )

        return text

    except sr.WaitTimeoutError:

        print(
            "KAYA: Listening timed out."
        )

        return ""

    except sr.UnknownValueError:

        print(
            "KAYA: Could not understand the audio."
        )

        return ""

    except sr.RequestError as e:

        print(
            f"KAYA speech service error: {e}"
        )

        return ""

    except Exception as e:

        print(
            f"KAYA voice error: {e}"
        )

        return ""