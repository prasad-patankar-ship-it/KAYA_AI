import edge_tts
import asyncio
import os
import subprocess


# ==========================================
# GENERATE KAYA VOICE
# ==========================================

async def generate_voice(text, voice):

    output_file = os.path.abspath("kaya_voice.mp3")

    communicate = edge_tts.Communicate(
        text,
        voice
    )

    await communicate.save(output_file)

    return output_file


# ==========================================
# KAYA TEXT TO SPEECH
# ==========================================

def speak(text, language="English"):

    voices = {
        "English": "en-US-AriaNeural",
        "हिन्दी": "hi-IN-AnanyaNeural",
        "मराठी": "mr-IN-AarohiNeural"
    }

    voice = voices.get(
        language,
        "en-US-AriaNeural"
    )

    try:

        output_file = asyncio.run(
            generate_voice(
                text,
                voice
            )
        )

        # ==================================
        # PLAY MP3 USING WINDOWS MEDIA PLAYER
        # ==================================

        if os.path.exists(output_file):

            subprocess.Popen(
                [
                    "wmplayer.exe",
                    output_file
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    except Exception as e:

        print(
            f"KAYA TTS error: {e}"
        )