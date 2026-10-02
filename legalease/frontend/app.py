"""
LegalEase Streamlit Frontend
"""

import os
from pathlib import Path

import requests
import streamlit as st

from dotenv import load_dotenv

from backend.utils.formatters import (
    format_docx,
    format_pdf,
    format_txt,
)

from backend.utils.text_utils import (
    html_escape,
)


load_dotenv()


APP_NAME = os.getenv(
    "APP_NAME",
    "LegalEase"
)


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# Optional logo
LOGO_PATH = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "logo.png"
)


# Streamlit configuration
st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS
st.markdown(
    """
<style>

.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 1.5rem;
}

.preview-card {
    background: #151515;
    color: #f2f2f2;
    padding: 24px;
    border-radius: 12px;
    min-height: 420px;
    max-height: 650px;
    overflow-y: auto;
    white-space: pre-wrap;
    font-family: Georgia, serif;
    line-height: 1.65;
}

</style>
""",
    unsafe_allow_html=True,
)


# Session state
if "generated_text" not in st.session_state:

    st.session_state.generated_text = ""


if "editing" not in st.session_state:

    st.session_state.editing = False


# Header
left, center, right = st.columns(
    [1, 2, 1]
)


with center:

    if LOGO_PATH.exists():

        st.image(
            str(LOGO_PATH),
            width=100
        )


    st.markdown(
        f"""
        <div class="main-title">
            {APP_NAME}
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="subtitle">
            AI-Powered Legal Document Generator
        </div>
        """,
        unsafe_allow_html=True,
    )


# Disclaimer
st.info(
    "LegalEase creates document drafts for "
    "informational purposes. It is not a substitute "
    "for advice from a qualified legal professional."
)


# Sidebar
with st.sidebar:

    st.header(
        "Document Inputs"
    )


    document_type = st.text_input(
        "Document Type",
        value="Freelance Work Contract"
    )


    parties = st.text_area(
        "Parties Involved",
        value=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=110,
    )


    terms = st.text_area(
        "Terms & Conditions",
        value=(
            "Payment within 30 days of invoice;"
            "Provider delivers work by the agreed deadline;"
            "Confidentiality must be maintained;"
            "Either party may terminate with 15 days notice"
        ),
        height=170,
        help=(
            "Separate individual terms using semicolon (;)."
        ),
    )


    dates = st.text_input(
        "Effective Date",
        value="October 2, 2026"
    )


    generate = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )


# Generate button
if generate:

    # Validate input
    if not all(
        [
            document_type.strip(),
            parties.strip(),
            terms.strip(),
            dates.strip(),
        ]
    ):

        st.error(
            "Please complete all four required inputs."
        )

    else:

        payload = {

            "document_type": document_type,

            "parties": parties,

            "terms": terms,

            "dates": dates,
        }


        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )


                response.raise_for_status()


                data = response.json()


                st.session_state.generated_text = (
                    data["generated_text"]
                )


                st.session_state.editing = False


                st.success(
                    "Document generated successfully."
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI backend. "
                    "Make sure the backend is running."
                )


            except requests.exceptions.Timeout:

                st.error(
                    "The backend took too long to respond. "
                    "Please try again."
                )


            except requests.exceptions.HTTPError:

                try:

                    detail = response.json().get(
                        "detail",
                        "Unknown error"
                    )

                except Exception:

                    detail = "Unknown backend error"


                st.error(
                    f"Generation failed: {detail}"
                )


# Show generated document
if st.session_state.generated_text:

    st.subheader(
        "Document Preview"
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button(
            "Click to Edit Document",
            use_container_width=True,
        ):

            st.session_state.editing = True


    with col2:

        if st.button(
            "Refresh Preview",
            use_container_width=True,
        ):

            st.session_state.editing = False


    # Editing mode
    if st.session_state.editing:

        edited = st.text_area(
            "Editable Document",
            value=st.session_state.generated_text,
            height=600,
        )


        st.session_state.generated_text = edited


    # Preview mode
    else:

        safe_text = html_escape(
            st.session_state.generated_text
        )


        st.markdown(
            f"""
            <div class="preview-card">
                {safe_text}
            </div>
            """,
            unsafe_allow_html=True,
        )


    # Downloads
    st.subheader(
        "Download Document"
    )


    col1, col2, col3 = st.columns(3)


    # TXT
    text_bytes = format_txt(
        st.session_state.generated_text
    )


    # DOCX
    docx_bytes = format_docx(
        st.session_state.generated_text,
        document_type,
        terms,
        (
            str(LOGO_PATH)
            if LOGO_PATH.exists()
            else None
        ),
    )


    # PDF
    pdf_bytes = format_pdf(
        st.session_state.generated_text,
        document_type,
        (
            str(LOGO_PATH)
            if LOGO_PATH.exists()
            else None
        ),
    )


    # Safe filename
    safe_name = "".join(
        character
        if (
            character.isalnum()
            or character in " _-"
        )
        else "_"
        for character in document_type.strip()
    ).strip().replace(
        " ",
        "_"
    )


    if not safe_name:

        safe_name = "legal_document"


    # TXT download
    with col1:

        st.download_button(
            "Download TXT",
            data=text_bytes,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )


    # DOCX download
    with col2:

        st.download_button(
            "Download DOCX",
            data=docx_bytes,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )


    # PDF download
    with col3:

        st.download_button(
            "Download PDF",
            data=pdf_bytes,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# Footer
st.divider()


st.caption(
    "LegalEase | AI-generated draft | "
    "Review important documents with a qualified legal professional."
)