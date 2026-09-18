"""Helpers for calling Ollama's OpenAI-compatible API."""

import base64
import io
import json
from collections.abc import Iterator, Sequence
from typing import Any

import requests
from PIL import Image

DEFAULT_OLLAMA_SERVER_URL = "http://host.docker.internal:11434/v1/chat/completions"
DEFAULT_OLLAMA_MODEL = "gemma4:12b"


def image_to_data_url(image_file: Any, max_size: int = 1280) -> str:
    """Convert an uploaded image to a compressed JPEG data URL."""
    image_file.seek(0)
    image = Image.open(image_file)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.thumbnail((max_size, max_size))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded_image}"


def build_multimodal_content(image_files: Sequence[Any], prompt_text: str) -> list[dict[str, Any]]:
    """Build the multimodal message content expected by Ollama."""
    content: list[dict[str, Any]] = []

    for image_file in image_files:
        if image_file is None:
            continue
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": image_to_data_url(image_file)},
            }
        )

    content.append({"type": "text", "text": prompt_text.strip()})
    return content


def build_payload(content: list[dict[str, Any]], model: str) -> dict[str, Any]:
    """Build a low-temperature streaming chat completion request."""
    return {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "stream": True,
        "temperature": 0.2,
        "max_tokens": -1,
    }


def stream_completion(
    url: str,
    payload: dict[str, Any],
    timeout_seconds: int = 300,
) -> Iterator[str]:
    """Yield text chunks from an OpenAI-compatible SSE response."""
    try:
        with requests.post(
            url, json=payload, stream=True, timeout=timeout_seconds
        ) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                line_text = line.decode("utf-8").strip()
                if not line_text.startswith("data: "):
                    continue

                data_content = line_text[6:]
                if data_content == "[DONE]":
                    break

                try:
                    data = json.loads(data_content)
                except json.JSONDecodeError:
                    continue

                choices = data.get("choices", [])
                if choices:
                    content_chunk = choices[0].get("delta", {}).get("content")
                    if content_chunk:
                        yield content_chunk
    except requests.exceptions.Timeout as error:
        raise TimeoutError from error
    except requests.exceptions.ConnectionError as error:
        raise ConnectionError from error
