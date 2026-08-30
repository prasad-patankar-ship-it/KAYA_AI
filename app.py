import os
import streamlit as st
from ai import ask_kaya
from voice import listen
from tts import speak
from tts import generate_voice
import asyncio
from medication import (
    add_medication,
    load_medications,
    delete_medication,
    update_medication_status
)
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from documents import (
    add_document,
    load_documents,
    delete_document
)
from medicines import (
    process_medication_question,
    get_all_medications,
    get_medication_status,
    add_medicine_action,
    delete_medicine_action,
    complete_medicine_action
)

from local_ai import (
    ask_kaya_local,
    detect_intent
)
from reminders import reminder_message

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="KAYA AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* ==========================================
   KAYA GLOBAL THEME
   ========================================== */

.stApp {
    background-color: var(--kaya-bg) !important;
    color: var(--kaya-text) !important;
}


/* ==========================================
   MAIN TEXT
   ========================================== */

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stMarkdown div,
.stText,
p,
h1,
h2,
h3,
h4,
h5,
h6 {
    color: var(--kaya-text) !important;
}


/* ==========================================
   SIDEBAR
   ========================================== */

[data-testid="stSidebar"] {
    background-color: var(--kaya-sidebar) !important;
}

[data-testid="stSidebar"] * {
    color: var(--kaya-text) !important;
}


/* ==========================================
   SIDEBAR NAVIGATION
   ========================================== */

[data-testid="stSidebar"] label {
    color: var(--kaya-text) !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    color: var(--kaya-text) !important;
}


/* ==========================================
   SIDEBAR SELECTBOX
   ========================================== */

[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: var(--kaya-input) !important;
    border: 1px solid var(--kaya-border) !important;
    border-radius: 10px !important;
    min-height: 44px !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] span {
    color: var(--kaya-input-text) !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] input {
    color: var(--kaya-input-text) !important;
    background-color: transparent !important;
}

[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    color: var(--kaya-input-text) !important;
    fill: var(--kaya-input-text) !important;
}


/* ==========================================
   SELECTBOX DROPDOWN
   ========================================== */

div[role="listbox"] {
    background-color: var(--kaya-input) !important;
    border: 1px solid var(--kaya-border) !important;
}

div[role="option"] {
    background-color: var(--kaya-input) !important;
    color: var(--kaya-input-text) !important;
}

div[role="option"] span {
    color: var(--kaya-input-text) !important;
}

div[role="option"]:hover {
    background-color: var(--kaya-hover) !important;
}


/* ==========================================
   INPUT BOXES
   ========================================== */

input,
textarea {
    background-color: var(--kaya-input) !important;
    color: var(--kaya-input-text) !important;
    caret-color: var(--kaya-input-text) !important;
}

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
}


/* ==========================================
   TIME INPUT
   ========================================== */

[data-testid="stTimeInput"] input {
    background-color: var(--kaya-input) !important;
    color: var(--kaya-input-text) !important;
}


/* ==========================================
   BUTTONS
   ========================================== */

.stButton > button {
    background-color: var(--kaya-button) !important;
    color: var(--kaya-text) !important;
    border: 1px solid var(--kaya-border) !important;
}

.stButton > button:hover {
    background-color: var(--kaya-hover) !important;
    color: var(--kaya-text) !important;
}


/* ==========================================
   FORM SUBMIT BUTTON
   ========================================== */

[data-testid="stFormSubmitButton"] button {
    color: #ffffff !important;
}


/* ==========================================
   ALERT BOXES
   ========================================== */

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #111827 !important;
}


/* ==========================================
   METRICS
   ========================================== */

[data-testid="stMetricValue"] {
    color: var(--kaya-text) !important;
}

[data-testid="stMetricLabel"] {
    color: var(--kaya-secondary) !important;
}

[data-testid="stMetricDelta"] {
    color: var(--kaya-secondary) !important;
}


/* ==========================================
   CAPTIONS
   ========================================== */

.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--kaya-secondary) !important;
}


/* ==========================================
   EXPANDERS
   ========================================== */

[data-testid="stExpander"] {
    background-color: var(--kaya-sidebar) !important;
    border-color: var(--kaya-border) !important;
}

[data-testid="stExpander"] * {
    color: var(--kaya-text) !important;
}


/* ==========================================
   CONTAINERS / CARDS
   ========================================== */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--kaya-sidebar) !important;
    border-color: var(--kaya-border) !important;
}


/* ==========================================
   CHAT
   ========================================== */

[data-testid="stChatMessage"] {
    color: var(--kaya-text) !important;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span {
    color: var(--kaya-text) !important;
}


/* ==========================================
   CHAT INPUT
   ========================================== */

[data-testid="stChatInput"] textarea {
    background-color: var(--kaya-input) !important;
    color: var(--kaya-input-text) !important;
}


/* ==========================================
   CHECKBOX
   ========================================== */

[data-testid="stCheckbox"] label {
    color: var(--kaya-text) !important;
}


/* ==========================================
   MAIN TITLES
   ========================================== */

.main-title {
    color: var(--kaya-text) !important;
    font-size: 32px;
    font-weight: 700;
}

.subtitle {
    color: var(--kaya-secondary) !important;
    font-size: 16px;
}

.section-title {
    color: var(--kaya-text) !important;
    font-size: 22px;
    font-weight: 600;
}


/* ==========================================
   DIVIDERS
   ========================================== */

hr {
    border-color: var(--kaya-border) !important;
}


/* ==========================================
   DATAFRAME
   ========================================== */

[data-testid="stDataFrame"] {
    color: #111827 !important;
}


/* ==========================================
   FILE UPLOADER
   ========================================== */

[data-testid="stFileUploader"] {
    color: var(--kaya-text) !important;
}

[data-testid="stFileUploader"] label {
    color: var(--kaya-text) !important;
}


/* ==========================================
   AUDIO
   ========================================== */

audio {
    width: 100% !important;
}


/* ==========================================
   MOBILE
   ========================================== */

@media (max-width: 768px) {

    .main-title {
        font-size: 26px !important;
    }

    .subtitle {
        font-size: 14px !important;
    }

    .section-title {
        font-size: 19px !important;
    }

    .stButton > button {
        min-height: 44px !important;
        font-size: 15px !important;
    }

    input,
    textarea {
        font-size: 16px !important;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 16px !important;
    }

    audio {
        width: 100% !important;
    }
}


/* ==========================================
   SMALL PHONE
   ========================================== */

@media (max-width: 480px) {

    .main-title {
        font-size: 23px !important;
    }

    .section-title {
        font-size: 18px !important;
    }

    .stButton > button {
        width: 100% !important;
        min-height: 46px !important;
    }
}


/* ==========================================
   NO HORIZONTAL OVERFLOW
   ========================================== */

html,
body,
.stApp {
    overflow-x: hidden !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    # ==========================================
    # KAYA HEADER
    # ==========================================

    st.markdown("## 🩺 KAYA AI")

    st.caption(
        "Your multilingual healthcare companion"
    )

    st.divider()

    # ==========================================
    # NAVIGATION
    # ==========================================

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "💬 AI Assistant",
            "💊 Medication",
            "📄 Medical Reports",
            "👨‍👩‍👦 Caregiver"
        ],
        key="kaya_navigation"
    )

    st.divider()

    # ==========================================
    # LANGUAGE
    # ==========================================

    language = st.selectbox(
        "🌐 Language",
        [
            "English",
            "हिन्दी",
            "मराठी"
        ],
        key="kaya_language_selector"
    )

    st.divider()

    # ==========================================
    # THEME
    # ==========================================

    theme = st.selectbox(
        "🎨 Theme",
        [
            "Dark",
            "Light"
        ],
        key="kaya_theme_selector"
    )


# =========================================================
# THEME VARIABLES
# =========================================================

if theme == "Light":

    st.markdown("""
    <style>

    :root {
        --kaya-bg: #f8fafc;
        --kaya-sidebar: #ffffff;
        --kaya-text: #111827;
        --kaya-secondary: #475569;
        --kaya-border: #cbd5e1;
        --kaya-input: #ffffff;
        --kaya-input-text: #111827;
        --kaya-button: #e2e8f0;
        --kaya-hover: #cbd5e1;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    :root {
        --kaya-bg: #0b1220;
        --kaya-sidebar: #111827;
        --kaya-text: #f8fafc;
        --kaya-secondary: #cbd5e1;
        --kaya-border: #334155;
        --kaya-input: #1b2435;
        --kaya-input-text: #ffffff;
        --kaya-button: #1e293b;
        --kaya-hover: #334155;
    }

    </style>
    """, unsafe_allow_html=True)

# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">🩺 Welcome to KAYA AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Healthcare technology that speaks your language.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # ==========================================
    # QUICK OVERVIEW
    # ==========================================

    medications = load_medications()

    total_medicines = len(medications)

    completed = sum(
        1
        for medicine in medications
        if medicine.get("status", "Upcoming") == "Completed"
    )

    pending = total_medicines - completed

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💊 Medicines",
            total_medicines
        )

    with col2:

        st.metric(
            "✅ Completed",
            completed
        )

    with col3:

        st.metric(
            "⏳ Pending",
            pending
        )

    st.divider()

    # ==========================================
    # TODAY'S MEDICATION
    # ==========================================

    st.markdown(
        '<div class="section-title">'
        '💊 Today\'s Medication'
        '</div>',
        unsafe_allow_html=True
    )

    if not medications:

        st.info(
            "No medication scheduled yet. "
            "Add medication from the Medication section."
        )

    else:

        for index, medicine in enumerate(medications):

            name = medicine.get(
                "name",
                "Medicine"
            )

            time = medicine.get(
                "time",
                "--:--"
            )

            instructions = medicine.get(
                "instructions",
                ""
            )

            status = medicine.get(
                "status",
                "Upcoming"
            )

            col1, col2, col3 = st.columns(
                [3, 2, 2]
            )

            with col1:

                st.write(
                    f"💊 **{name}**"
                )

                if instructions:

                    st.caption(
                        f"📝 {instructions}"
                    )

            with col2:

                st.write(
                    f"🕐 {time}"
                )

            with col3:

                if status == "Completed":

                    st.success(
                        "✓ Done"
                    )

                else:

                    if st.button(
                        "✅ Mark Done",
                        key=f"home_done_{index}",
                        use_container_width=True
                    ):

                        update_medication_status(
                            index,
                            "Completed"
                        )

                        st.rerun()

            st.divider()

        # Progress

        st.write(
            f"📊 **Today's progress: "
            f"{completed}/{total_medicines} completed**"
        )

    st.divider()

    # ==========================================
    # KAYA FEATURES
    # ==========================================

    st.markdown(
        '<div class="section-title">'
        '✨ KAYA Capabilities'
        '</div>',
        unsafe_allow_html=True
    )

    feature1, feature2, feature3 = st.columns(3)

    with feature1:

        st.markdown(
            """
            ### 🧠 AI Assistant

            Ask KAYA healthcare questions,
            medication questions, or interact
            using voice.
            """
        )

    with feature2:

        st.markdown(
            """
            ### 🌐 Multilingual

            Communicate with KAYA in
            English, Hindi, or Marathi.
            """
        )

    with feature3:

        st.markdown(
            """
            ### 📄 Medical Reports

            Upload reports and get a
            simple AI-generated explanation.
            """
        )

    st.divider()

    # ==========================================
    # QUICK ACTIONS
    # ==========================================

    st.markdown(
        '<div class="section-title">'
        '⚡ Quick Actions'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "💡 Use the sidebar to open "
        "AI Assistant, Medication, "
        "Medical Reports, or Caregiver."
    )

    # ==========================================
    # SAFETY NOTE
    # ==========================================

    st.caption(
        "ℹ️ KAYA provides general healthcare information "
        "and medication assistance. It does not replace "
        "a qualified healthcare professional."
    )
# =========================================================
# AI ASSISTANT
# =========================================================
# =========================================================
# AI ASSISTANT
# =========================================================

elif page == "💬 AI Assistant":

    st.markdown(
        '<div class="main-title">💬 KAYA AI Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Ask KAYA by typing or speaking.'
        '</div>',
        unsafe_allow_html=True
    )

    # ==========================================
    # CHAT MEMORY
    # ==========================================

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # ==========================================
    # SHOW CHAT HISTORY
    # ==========================================

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # ==========================================
    # KAYA RESPONSE ENGINE
    # ==========================================

    def get_kaya_response(user_message):

        # ======================================
        # 1. DIRECT MEDICATION QUESTIONS
        # ======================================

        try:

            medication_response = (
                process_medication_question(
                    user_message,
                    language
                )
            )

            if medication_response:

                return medication_response

        except Exception as e:

            print(
                f"Medication processing error: {e}"
            )

        # ======================================
        # 2. LOCAL QWEN INTENT DETECTION
        # ======================================

        try:

            intent_data = detect_intent(
                user_message
            )

            intent = intent_data.get(
                "intent",
                "GENERAL_QUESTION"
            )

            medicine_name = intent_data.get(
                "medicine_name",
                ""
            )

            medicine_time = intent_data.get(
                "time",
                ""
            )

            instructions = intent_data.get(
                "instructions",
                ""
            )

            frequency = intent_data.get(
                "frequency",
                "Daily"
            )

            # ==================================
            # ADD MEDICINE
            # ==================================

            if intent == "ADD_MEDICINE":

                if medicine_name and medicine_time:

                    return add_medicine_action(
                        medicine_name,
                        medicine_time,
                        instructions,
                        frequency,
                        language
                    )

                if language == "हिन्दी":

                    return (
                        "कृपया दवाई का नाम "
                        "और समय बताएं।"
                    )

                if language == "मराठी":

                    return (
                        "कृपया औषधाचे नाव "
                        "आणि वेळ सांगा."
                    )

                return (
                    "Please tell me the medicine "
                    "name and time."
                )

            # ==================================
            # DELETE MEDICINE
            # ==================================

            if intent == "DELETE_MEDICINE":

                if medicine_name:

                    return delete_medicine_action(
                        medicine_name,
                        language
                    )

                return (
                    "Please tell me which medicine "
                    "you want to delete."
                )

            # ==================================
            # COMPLETE MEDICINE
            # ==================================

            if intent == "COMPLETE_MEDICINE":

                if medicine_name:

                    return complete_medicine_action(
                        medicine_name,
                        language
                    )

                return (
                    "Please tell me which medicine "
                    "you completed."
                )

            # ==================================
            # SHOW MEDICINES
            # ==================================

            if intent == "SHOW_MEDICINES":

                return get_all_medications(
                    language
                )

            # ==================================
            # CHECK DUE MEDICINE
            # ==================================

            if intent == "CHECK_DUE_MEDICINE":

                return get_medication_status(
                    language
                )

        except Exception as e:

            print(
                f"Intent detection error: {e}"
            )

        # ======================================
        # 3. BUILD CONVERSATION MEMORY
        # ======================================

        conversation = ""

        previous_messages = (
            st.session_state.messages[-6:]
        )

        for message in previous_messages:

            role = message.get(
                "role",
                "user"
            )

            content = message.get(
                "content",
                ""
            )

            conversation += (
                f"{role}: {content}\n"
            )

        # ======================================
        # 4. LOAD CURRENT MEDICATIONS
        # ======================================

        medications = load_medications()

        medication_context = ""

        if medications:

            medication_context = (
                "\nCURRENT SAVED MEDICATIONS:\n"
            )

            for medicine in medications:

                medication_context += (
                    f"- {medicine.get('name', '')} "
                    f"at {medicine.get('time', '')} "
                    f"| Instructions: "
                    f"{medicine.get('instructions', '')} "
                    f"| Status: "
                    f"{medicine.get('status', 'Upcoming')}\n"
                )

        else:

            medication_context = (
                "\nCURRENT SAVED MEDICATIONS:\n"
                "No medications are currently saved.\n"
            )

        # ======================================
        # 5. LOCAL QWEN
        # ======================================

        try:

            enhanced_prompt = f"""
You are KAYA, a friendly multilingual
healthcare assistant.

The user's selected language is:
{language}

Always answer in the user's selected language.

Use the conversation history when relevant.

Use the saved medication information when
relevant.

Never invent a medicine, dosage, prescription,
diagnosis, or medical record.

Give general health information only.

For important medical concerns, recommend
consulting a qualified healthcare professional.

CONVERSATION HISTORY:
{conversation}

{medication_context}

CURRENT USER MESSAGE:
{user_message}

Answer naturally and concisely as KAYA.
"""

            return ask_kaya_local(
                enhanced_prompt,
                language
            )

        except Exception as e:

            return (
                f"KAYA could not respond: {e}"
            )

    # ==========================================
    # TEXT CHAT
    # ==========================================

    user_message = st.chat_input(
        "Ask KAYA anything..."
    )

    if user_message:

        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })

        with st.chat_message("user"):

            st.write(
                user_message
            )

        with st.chat_message("assistant"):

            with st.spinner(
                "KAYA is thinking..."
            ):

                response = get_kaya_response(
                    user_message
                )

            st.write(
                response
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        # ======================================
        # BROWSER AUDIO
        # ======================================

        try:

            voices = {
                "English": "en-US-AriaNeural",
                "हिन्दी": "hi-IN-AnanyaNeural",
                "मराठी": "mr-IN-AarohiNeural"
            }

            selected_voice = voices.get(
                language,
                "en-US-AriaNeural"
            )

            audio_file = asyncio.run(
                generate_voice(
                    response,
                    selected_voice
                )
            )

            with open(
                audio_file,
                "rb"
            ) as audio_handle:

                audio_bytes = audio_handle.read()

            st.audio(
                audio_bytes,
                format="audio/mpeg"
            )

        except Exception as e:

            print(
                f"TTS error: {e}"
            )

    # ==========================================
    # PC VOICE INPUT
    # KEEPING YOUR EXISTING FEATURE
    # ==========================================

    st.divider()

    if st.button(
        "🎙️ Speak to KAYA (PC)",
        use_container_width=True
    ):

        with st.spinner(
            "🎙️ KAYA is listening..."
        ):

            voice_text = listen(
                language
            )

        if not voice_text:

            st.warning(
                "KAYA could not understand "
                "the voice input."
            )

        else:

            st.session_state.messages.append({
                "role": "user",
                "content": voice_text
            })

            with st.chat_message("user"):

                st.write(
                    voice_text
                )

            with st.chat_message("assistant"):

                with st.spinner(
                    "KAYA is thinking..."
                ):

                    response = get_kaya_response(
                        voice_text
                    )

                st.write(
                    response
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            try:

                voices = {
                    "English": "en-US-AriaNeural",
                    "हिन्दी": "hi-IN-AnanyaNeural",
                    "मराठी": "mr-IN-AarohiNeural"
                }

                selected_voice = voices.get(
                    language,
                    "en-US-AriaNeural"
                )

                audio_file = asyncio.run(
                    generate_voice(
                        response,
                        selected_voice
                    )
                )

                with open(
                    audio_file,
                    "rb"
                ) as audio_handle:

                    audio_bytes = audio_handle.read()

                st.audio(
                    audio_bytes,
                    format="audio/mpeg"
                )

            except Exception as e:

                print(
                    f"PC TTS error: {e}"
                )

    # ==========================================
    # ANDROID / BROWSER VOICE INPUT
    # ==========================================

    st.divider()

    st.markdown(
        "### 📱 Android Voice"
    )

    st.caption(
        "Tap the microphone, speak, and KAYA "
        "will process your request."
    )

    android_audio = st.audio_input(
        "🎙️ Tap to speak to KAYA",
        key="android_kaya_voice"
    )

    if android_audio:

        try:

            import io
            import speech_recognition as sr

            recognizer = sr.Recognizer()

            language_codes = {
                "English": "en-IN",
                "हिन्दी": "hi-IN",
                "मराठी": "mr-IN"
            }

            speech_language = language_codes.get(
                language,
                "en-IN"
            )

            audio_data = (
                android_audio.getvalue()
            )

            audio_stream = io.BytesIO(
                audio_data
            )

            with sr.AudioFile(
                audio_stream
            ) as source:

                recorded_audio = (
                    recognizer.record(
                        source
                    )
                )

            with st.spinner(
                "🎙️ KAYA is understanding you..."
            ):

                voice_text = (
                    recognizer.recognize_google(
                        recorded_audio,
                        language=speech_language
                    )
                )

            if voice_text:

                st.session_state.messages.append({
                    "role": "user",
                    "content": voice_text
                })

                with st.chat_message("user"):

                    st.write(
                        voice_text
                    )

                with st.chat_message(
                    "assistant"
                ):

                    with st.spinner(
                        "KAYA is thinking..."
                    ):

                        response = (
                            get_kaya_response(
                                voice_text
                            )
                        )

                    st.write(
                        response
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

                # ==================================
                # ANDROID AUDIO RESPONSE
                # ==================================

                try:

                    voices = {
                        "English": "en-US-AriaNeural",
                        "हिन्दी": "hi-IN-AnanyaNeural",
                        "मराठी": "mr-IN-AarohiNeural"
                    }

                    selected_voice = voices.get(
                        language,
                        "en-US-AriaNeural"
                    )

                    audio_file = asyncio.run(
                        generate_voice(
                            response,
                            selected_voice
                        )
                    )

                    with open(
                        audio_file,
                        "rb"
                    ) as audio_handle:

                        audio_bytes = (
                            audio_handle.read()
                        )

                    st.markdown(
                        "🔊 **KAYA Voice Response**"
                    )

                    st.audio(
                        audio_bytes,
                        format="audio/mpeg"
                    )

                except Exception as e:

                    st.warning(
                        f"Voice response unavailable: {e}"
                    )

        except sr.UnknownValueError:

            st.warning(
                "KAYA could not understand you. "
                "Please speak clearly and try again."
            )

        except sr.RequestError:

            st.error(
                "Speech recognition service is unavailable."
            )

        except Exception as e:

            st.error(
                f"Android voice error: {e}"
            )
# =========================================================
# MEDICATION
# =========================================================

elif page == "💊 Medication":

    st.markdown(
        '<div class="main-title">💊 Medication Manager</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Manage your medicines and daily schedule.'
        '</div>',
        unsafe_allow_html=True
    )

    # ==============================
    # ADD MEDICINE
    # ==============================

    st.subheader("➕ Add Medicine")

    with st.form("add_medicine_form"):

        medicine_name = st.text_input(
            "Medicine Name",
            placeholder="e.g. Paracetamol"
        )

        medicine_time = st.time_input(
            "Medication Time"
        )

        medicine_frequency = st.selectbox(
            "Frequency",
            [
                "Daily",
                "Twice Daily",
                "Weekly",
                "As Needed"
            ]
        )

        medicine_instructions = st.text_input(
            "Instructions",
            placeholder="e.g. After food"
        )

        submitted = st.form_submit_button(
            "💾 Save Medicine",
            use_container_width=True
        )

        if submitted:

            if medicine_name.strip():

                add_medication(
                    medicine_name.strip(),
                    medicine_time.strftime("%H:%M"),
                    medicine_instructions.strip(),
                    medicine_frequency
                )

                st.success(
                    f"✅ {medicine_name} added successfully!"
                )

                st.rerun()

            else:

                st.warning(
                    "Please enter a medicine name."
                )

    st.divider()

    # ==============================
    # SAVED MEDICINES
    # ==============================

    st.subheader("📋 Your Medicines")

    medications = load_medications()

    if not medications:

        st.info(
            "No medicines added yet."
        )

    else:

        for index, medicine in enumerate(medications):

            name = medicine.get(
                "name",
                "Unknown Medicine"
            )

            time = medicine.get(
                "time",
                "--:--"
            )

            frequency = medicine.get(
                "frequency",
                "Daily"
            )

            instructions = medicine.get(
                "instructions",
                "No instructions"
            )

            status = medicine.get(
                "status",
                "Upcoming"
            )

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [3, 2, 1]
                )

                # Medicine information
                with col1:

                    st.markdown(
                        f"### 💊 {name}"
                    )

                    st.write(
                        f"📝 {instructions}"
                    )

                # Time and status
                with col2:

                    st.write(
                        f"🕐 **{time}**"
                    )

                    st.write(
                        f"🔄 {frequency}"
                    )

                    if status == "Completed":

                        st.success("✓ Completed")

                    else:

                        st.info("⏳ Upcoming")

                # Actions
                with col3:

                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_medicine_{index}",
                        use_container_width=True
                    ):

                        delete_medication(index)

                        st.rerun()

                    if status != "Completed":

                        if st.button(
                            "✅ Done",
                            key=f"complete_medicine_{index}",
                            use_container_width=True
                        ):

                            update_medication_status(
                                index,
                                "Completed"
                            )

                            st.rerun()
# =========================================================
# MEDICAL REPORTS
# =========================================================

elif page == "📄 Medical Reports":

    st.markdown(
        '<div class="main-title">📄 Medical Reports</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Upload, read, download and manage your medical reports.'
        '</div>',
        unsafe_allow_html=True
    )

    # ==========================================
    # REPORT STORAGE
    # ==========================================

    REPORT_FOLDER = "medical_reports"

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    # ==========================================
    # UPLOAD REPORT
    # ==========================================

    st.markdown(
        '<div class="section-title">'
        '📤 Upload Medical Report'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_report = st.file_uploader(
        "Choose a medical report",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg"
        ],
        key="medical_report_uploader"
    )

    if uploaded_report is not None:

        safe_filename = os.path.basename(
            uploaded_report.name
        )

        report_path = os.path.join(
            REPORT_FOLDER,
            safe_filename
        )

        try:

            with open(
                report_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_report.getbuffer()
                )

            st.success(
                f"✅ {safe_filename} uploaded successfully."
            )

        except Exception as e:

            st.error(
                f"Could not save report: {e}"
            )

    st.divider()

    # ==========================================
    # SAVED REPORTS
    # ==========================================

    st.markdown(
        '<div class="section-title">'
        '📚 Saved Reports'
        '</div>',
        unsafe_allow_html=True
    )

    report_files = []

    try:

        report_files = sorted(
            [
                filename
                for filename in os.listdir(
                    REPORT_FOLDER
                )
                if filename.lower().endswith(
                    (
                        ".pdf",
                        ".png",
                        ".jpg",
                        ".jpeg"
                    )
                )
            ]
        )

    except Exception as e:

        st.error(
            f"Could not load reports: {e}"
        )

    # ==========================================
    # NO REPORTS
    # ==========================================

    if not report_files:

        st.info(
            "No medical reports uploaded yet."
        )

    # ==========================================
    # DISPLAY REPORTS
    # ==========================================

    else:

        for index, filename in enumerate(
            report_files
        ):

            report_path = os.path.join(
                REPORT_FOLDER,
                filename
            )

            st.markdown(
                f"### 📄 {filename}"
            )

            # ----------------------------------
            # ACTION BUTTONS
            # ----------------------------------

            col1, col2 = st.columns(2)

            # ==================================
            # VIEW
            # ==================================

            with col1:

                view_report = st.button(
                    "👁️ View / Read",
                    key=f"view_report_{index}",
                    use_container_width=True
                )

            # ==================================
            # DELETE
            # ==================================

            with col2:

                delete_report = st.button(
                    "🗑️ Delete",
                    key=f"delete_report_{index}",
                    use_container_width=True
                )

            # ==================================
            # DOWNLOAD
            # ==================================

            try:

                with open(
                    report_path,
                    "rb"
                ) as report_file:

                    report_bytes = (
                        report_file.read()
                    )

                st.download_button(
                    "⬇️ Download Report",
                    data=report_bytes,
                    file_name=filename,
                    mime=(
                        "application/pdf"
                        if filename.lower().endswith(".pdf")
                        else "image/jpeg"
                    ),
                    key=f"download_report_{index}",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"Could not open file: {e}"
                )

            # ==================================
            # VIEW REPORT
            # ==================================

            if view_report:

                extension = os.path.splitext(
                    filename
                )[1].lower()

                try:

                    if extension == ".pdf":

                        st.markdown(
                            "#### 📖 Report Viewer"
                        )

                        st.pdf(
                            report_path,
                            height=700
                        )

                    elif extension in [
                        ".png",
                        ".jpg",
                        ".jpeg"
                    ]:

                        st.markdown(
                            "#### 📖 Report Viewer"
                        )

                        st.image(
                            report_path,
                            use_container_width=True
                        )

                except Exception as e:

                    st.error(
                        f"Could not display report: {e}"
                    )

            # ==================================
            # DELETE REPORT
            # ==================================

            if delete_report:

                try:

                    if os.path.exists(
                        report_path
                    ):

                        os.remove(
                            report_path
                        )

                        st.success(
                            f"🗑️ {filename} deleted."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Report was already deleted."
                        )

                except Exception as e:

                    st.error(
                        f"Could not delete report: {e}"
                    )

            st.divider()

    # ==========================================
    # INFORMATION
    # ==========================================

    st.caption(
        "🔒 Reports are stored locally in the "
        "'medical_reports' folder of KAYA."
    )

    st.caption(
        "ℹ️ KAYA can display uploaded PDFs and "
        "images. AI interpretation should be treated "
        "as informational and not as a medical diagnosis."
    )
# =========================================================
# CAREGIVER
# =========================================================

elif page == "👨‍👩‍👦 Caregiver":

    st.markdown(
        '<div class="main-title">👨‍👩‍👦 Caregiver Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Medication routine overview for caregivers.'
        '</div>',
        unsafe_allow_html=True
    )

    # ==========================================
    # LOAD MEDICATIONS
    # ==========================================

    medications = load_medications()

    total = len(medications)

    completed = sum(
        1
        for medicine in medications
        if medicine.get("status", "Upcoming") == "Completed"
    )

    pending = total - completed

    # ==========================================
    # SUMMARY
    # ==========================================

    st.markdown(
        '<div class="section-title">📊 Today\'s Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💊 Total Medicines",
            total
        )

    with col2:
        st.metric(
            "✅ Completed",
            completed
        )

    with col3:
        st.metric(
            "⏳ Pending",
            pending
        )

    st.divider()

    # ==========================================
    # MEDICATION ACTIVITY
    # ==========================================

    st.markdown(
        '<div class="section-title">💊 Medication Activity</div>',
        unsafe_allow_html=True
    )

    if not medications:

        st.info(
            "No medicines have been added yet."
        )

    else:

        for medicine in medications:

            name = medicine.get(
                "name",
                "Medicine"
            )

            time = medicine.get(
                "time",
                "--:--"
            )

            instructions = medicine.get(
                "instructions",
                ""
            )

            status = medicine.get(
                "status",
                "Upcoming"
            )

            col1, col2, col3 = st.columns(
                [3, 2, 2]
            )

            with col1:

                st.write(
                    f"💊 **{name}**"
                )

                if instructions:

                    st.caption(
                        f"📝 {instructions}"
                    )

            with col2:

                st.write(
                    f"🕐 {time}"
                )

            with col3:

                if status == "Completed":

                    st.success(
                        "✓ Completed"
                    )

                else:

                    st.warning(
                        "⏳ Upcoming"
                    )

            st.divider()

    # ==========================================
    # CAREGIVER INFORMATION
    # ==========================================

    st.markdown(
        '<div class="section-title">ℹ️ Caregiver Information</div>',
        unsafe_allow_html=True
    )

    st.info(
        "KAYA provides a medication routine overview "
        "for caregivers. Medication status represents "
        "interaction with the medication schedule and "
        "does not prove that a medicine was actually "
        "ingested."
    )