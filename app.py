import smtplib
import time
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT


# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------

st.set_page_config(
    page_title="VerifyLens AI",
    page_icon="🔎",
    layout="centered",
)


# -------------------------------------------------------------------
# Gemini client
# -------------------------------------------------------------------

@st.cache_resource
def get_client():
    """Create and cache the Gemini client."""
    api_key = st.secrets["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)


# -------------------------------------------------------------------
# Email
# -------------------------------------------------------------------

def send_email(to_address, subject, body):
    """Send a review report through Gmail SMTP."""
    gmail_address = st.secrets["GMAIL_ADDRESS"]
    app_password = st.secrets["GMAIL_APP_PASSWORD"]

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = gmail_address
    message["To"] = to_address

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, app_password)
        server.send_message(message)


# -------------------------------------------------------------------
# Gemini chat
# -------------------------------------------------------------------

def create_chat():
    """Create a new VerifyLens Gemini conversation."""
    client = get_client()

    return client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )


def ask_gemini(parts):
    """Send a message to Gemini with automatic retry for 503 errors."""

    for attempt in range(3):
        try:
            response = st.session_state.chat.send_message(parts)
            return response.text

        except Exception as error:
            error_text = str(error)

            if (
                "503" in error_text
                or "UNAVAILABLE" in error_text
            ):
                if attempt < 2:
                    time.sleep(3)
                    continue

            raise


# -------------------------------------------------------------------
# Session initialization
# -------------------------------------------------------------------

def initialize_session():
    """Initialize the application session."""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "onboarded" not in st.session_state:
        st.session_state.onboarded = False


def start_new_review():
    """Reset the current review session."""

    st.session_state.messages = []
    st.session_state.chat = create_chat()


# -------------------------------------------------------------------
# Initialize
# -------------------------------------------------------------------

initialize_session()


# -------------------------------------------------------------------
# Onboarding
# -------------------------------------------------------------------

if not st.session_state.onboarded:

    st.title("🔎 VerifyLens AI")

    st.caption(
        "See the evidence. Understand the uncertainty. "
        "Keep humans in control."
    )

    st.info(
        "VerifyLens provides AI-assisted visual analysis. "
        "It does not replace physical inspection or human "
        "decision-making."
    )

    st.subheader("Let's get started")

    with st.form("onboarding_form"):

        name = st.text_input(
            "Your name",
            placeholder="Enter your name",
        )

        email = st.text_input(
            "Report recipient email",
            placeholder="example@gmail.com",
        )

        submitted = st.form_submit_button(
            "Start Review 🚀",
            use_container_width=True,
        )

    if submitted:

        if not name.strip() or not email.strip():

            st.warning(
                "Please fill in both your name and email address."
            )

        else:

            st.session_state.name = name.strip()
            st.session_state.email = email.strip()

            st.session_state.chat = create_chat()
            st.session_state.messages = []

            st.session_state.onboarded = True

            st.rerun()

    st.stop()


# -------------------------------------------------------------------
# Main application
# -------------------------------------------------------------------

st.title("🔎 VerifyLens AI")

st.caption(
    f"Welcome, {st.session_state.name}. "
    "Upload visual evidence or ask a question."
)

st.info(
    "VerifyLens provides AI-assisted visual analysis. "
    "Important decisions should be verified by a qualified human."
)


# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------

with st.sidebar:

    st.header("Review")

    st.write(
        f"**Reviewer:** {st.session_state.name}"
    )

    st.write(
        f"**Report email:** {st.session_state.email}"
    )

    st.divider()

    if st.button(
        "🔄 Start New Review",
        use_container_width=True,
    ):

        start_new_review()
        st.rerun()

    st.divider()

    st.subheader("Responsible AI")

    st.markdown(
        """
        **VerifyLens is designed to:**

        - Separate observations from interpretations
        - Identify uncertainty
        - Avoid invented information
        - Recommend human review when needed
        - Keep final decisions with people
        """
    )


# -------------------------------------------------------------------
# Display conversation history
# -------------------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message.get("image") is not None:
            st.image(message["image"])

        if message.get("content"):
            st.markdown(message["content"])


# -------------------------------------------------------------------
# Input
# -------------------------------------------------------------------

uploaded_image = st.file_uploader(
    "Upload visual evidence",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
    help=(
        "Upload a photo of the item or situation "
        "you want VerifyLens to review."
    ),
)

user_text = st.chat_input(
    "Describe what you want VerifyLens to check..."
)


# -------------------------------------------------------------------
# Process user input
# -------------------------------------------------------------------

if user_text or uploaded_image:

    parts = []

    image_bytes = None

    # ---------------------------------------------------------------
    # Image
    # ---------------------------------------------------------------

    if uploaded_image:

        image_bytes = uploaded_image.getvalue()

        parts.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=uploaded_image.type,
            )
        )

    # ---------------------------------------------------------------
    # Text
    # ---------------------------------------------------------------

    if user_text:

        parts.append(user_text)

    else:

        parts.append(
            "Analyze this image using the VerifyLens "
            "evidence-based visual verification framework."
        )

    # ---------------------------------------------------------------
    # Save user message
    # ---------------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": (
                user_text
                or "Please analyze this image."
            ),
            "image": image_bytes,
        }
    )

    # ---------------------------------------------------------------
    # Display user message
    # ---------------------------------------------------------------

    with st.chat_message("user"):

        if uploaded_image:
            st.image(uploaded_image)

        st.markdown(
            user_text
            or "Please analyze this image."
        )

    # ---------------------------------------------------------------
    # Gemini response
    # ---------------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Analyzing the available evidence..."
        ):

            try:

                answer = ask_gemini(parts)

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "image": None,
                    }
                )

            except Exception as error:

                error_text = str(error)

                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                ):

                    st.warning(
                        "Gemini is temporarily busy. "
                        "Please try again in a few seconds."
                    )

                else:

                    st.error(
                        "I couldn't complete the analysis. "
                        "Please check your Gemini API configuration "
                        "and try again."
                    )

                with st.expander(
                    "Technical details"
                ):

                    st.code(error_text)


# -------------------------------------------------------------------
# Review report
# -------------------------------------------------------------------

assistant_messages = [
    message["content"]
    for message in st.session_state.messages
    if message["role"] == "assistant"
    and message.get("content")
]


if assistant_messages:

    st.divider()

    st.subheader("📧 Review Report")

    st.caption(
        f"The report will be sent to "
        f"{st.session_state.email}"
    )

    if st.button(
        "📤 Send Review Report",
        use_container_width=True,
    ):

        report = (
            f"VerifyLens AI — Visual Review Report\n\n"
            f"Reviewer: {st.session_state.name}\n\n"
            + "\n\n".join(assistant_messages)
        )

        with st.spinner(
            "Sending review report..."
        ):

            try:

                send_email(
                    st.session_state.email,
                    "VerifyLens AI - Visual Review Report",
                    report,
                )

                st.success(
                    "Review report sent successfully! 📧"
                )

            except Exception as error:

                st.error(
                    "The report could not be sent. "
                    "Please check your Gmail configuration."
                )

                with st.expander(
                    "Technical details"
                ):

                    st.code(str(error))
