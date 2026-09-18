"""Streamlit UI for the TTB label compliance verifier."""

import os
from typing import Any

import streamlit as st

from guideline_data import GUIDELINE_MAP
from ollama_client import (
    DEFAULT_OLLAMA_MODEL,
    build_multimodal_content,
    build_payload,
    stream_completion,
)
from prompt_builder import build_audit_prompt

OLLAMA_SERVER_URL = os.getenv(
    "OLLAMA_SERVER_URL",
    "http://host.docker.internal:11434/v1/chat/completions",
)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]


def render_header() -> None:
    """Render the application title and usage instructions."""
    st.title("Alcoholic Beverage Label Compliance Verifier")
    st.info(
        "**Prototype Notice:** This is a prototype for the Alcohol and Tobacco Tax and Trade Bureau (TTB). "
        "The application sends label images and declared metadata to a local OpenAI-compatible model.\n\n"
        "**How to use:** Select a category, subclass, and net contents; fill in the manifest details; "
        "upload label images; then execute verification."
    )


def render_inputs() -> dict[str, Any]:
    """Render input controls and return the user's selections."""
    with st.container(border=True):
        st.subheader("1. Classification and subclass selection")
        category_options = {
            key: data["section_name"] for key, data in GUIDELINE_MAP.items()
        }
        selected_sec_key = st.selectbox(
            "Select beverage category",
            options=list(category_options),
            format_func=category_options.get,
        )
        guideline = GUIDELINE_MAP[selected_sec_key]

        selected_subclass = st.selectbox(
            "Select subclass designation", guideline["class_types"]
        )
        selected_net_contents = st.selectbox(
            "Select net contents size", guideline["net_content_allowed_values"]
        )

        contains_sulfites = False
        if selected_sec_key == "4.2":
            contains_sulfites = st.checkbox(
                "Product contains 10+ ppm sulfites",
                value=True,
                help="Uncheck if this wine is naturally low in sulfites (<10 ppm).",
            )

        st.subheader("2. Application manifest details")
        app_id = st.text_input("Application ID", value="COLA-2026-001")
        brand_name = st.text_input("Brand name", value="DON Q")
        alcohol_content = st.text_input("Alcohol content", value="40% Alc./Vol.")
        company_name = st.text_input(
            "Company / manufacturer name",
            value="DESTILERIA SERRALLES, INC.",
        )
        location_address = st.text_input(
            "Bottler / producer location",
            value="PONCE, PUERTO RICO",
        )

        st.subheader("3. Label images")
        front_img = st.file_uploader("Upload front label image", type=IMAGE_TYPES)
        back_img = st.file_uploader("Upload back label image", type=IMAGE_TYPES)
        _render_image_previews(front_img, back_img)
        submit_button = st.button(
            "Verify label compliance",
            type="primary",
            width="stretch",
        )

    return {
        "guideline": guideline,
        "section_key": selected_sec_key,
        "selected_subclass": selected_subclass,
        "selected_net_contents": selected_net_contents,
        "contains_sulfites": contains_sulfites,
        "app_id": app_id,
        "brand_name": brand_name,
        "alcohol_content": alcohol_content,
        "company_name": company_name,
        "location_address": location_address,
        "front_img": front_img,
        "back_img": back_img,
        "submit_button": submit_button,
    }


def _render_image_previews(front_img: Any, back_img: Any) -> None:
    """Render uploaded image previews when available."""
    if not front_img and not back_img:
        return

    preview_col1, preview_col2 = st.columns(2)
    with preview_col1:
        if front_img:
            st.image(front_img, caption="Front label preview", width="stretch")
    with preview_col2:
        if back_img:
            st.image(back_img, caption="Back label preview", width="stretch")


def verify_label(inputs: dict[str, Any], result_container: Any) -> None:
    """Build an audit request and stream the model response to the UI."""
    front_img = inputs["front_img"]
    back_img = inputs["back_img"]
    if not (front_img or back_img):
        result_container.error("Please upload at least one label image.")
        return

    guideline = inputs["guideline"]
    result_container.info(
        f"Auditing via the local model for {guideline['section_name']} "
        f"({inputs['selected_subclass']})..."
    )

    prompt = build_audit_prompt(
        inputs["guideline"],
        section_key=inputs["section_key"],
        selected_subclass=inputs["selected_subclass"],
        selected_net_contents=inputs["selected_net_contents"],
        app_id=inputs["app_id"],
        brand_name=inputs["brand_name"],
        alcohol_content=inputs["alcohol_content"],
        company_name=inputs["company_name"],
        location_address=inputs["location_address"],
        contains_sulfites=inputs["contains_sulfites"],
    )
    content = build_multimodal_content([front_img, back_img], prompt)
    payload = build_payload(content, OLLAMA_MODEL)
    response_slot = result_container.empty()
    output_text = ""

    try:
        for chunk in stream_completion(OLLAMA_SERVER_URL, payload):
            output_text += chunk
            response_slot.markdown(output_text + "▌")
        response_slot.markdown(output_text or "The model returned no text.")
    except TimeoutError:
        result_container.error("The request timed out after 5 minutes.")
    except ConnectionError:
        result_container.error(
            f"Could not connect to the model endpoint at {OLLAMA_SERVER_URL}."
        )
    except Exception as error:
        result_container.error(f"Error communicating with the model: {error}")


st.set_page_config(page_title="TTB Label Compliance Verifier", layout="wide")
render_header()

col_input, col_output = st.columns([1, 1], gap="large")
with col_input:
    inputs = render_inputs()

with col_output:
    st.subheader("Verification results")
    result_container = st.container()
    if not inputs["submit_button"]:
        result_container.info(
            "Fill out the metadata, attach label images, and click **Verify label compliance**."
        )

if inputs["submit_button"]:
    verify_label(inputs, result_container)
