import json
import copy
import fitz
import base64
from google.genai import types
from core.llm.clients import google_client_async, openai_client_async


async def fetch_with_id(
    call_id: str,
    config: types.GenerateContentConfig,
    file_uri: str,
):
    response = await google_client_async.models.generate_content(
        model="gemini-3.1-pro-preview",
        config=config,
        contents=[
            types.Part.from_uri(file_uri=file_uri, mime_type="application/pdf"),
            "Analyze the given structural plan based on the provided instructions",
        ],
    )
    # Access the usage metadata here
    usage = response.usage_metadata
    print(f"--- Usage Stats for {call_id} ---")
    print(f"Input Tokens: {usage.prompt_token_count}")
    print(f"Thinking Tokens: {usage.thoughts_token_count}")
    print(f"Output Tokens (Actual Response): {usage.candidates_token_count}")
    print(f"Total Tokens: {usage.total_token_count}")
    return call_id, response.parsed


async def fetch_with_id_kimi(call_id: str, system_prompt: str, payload: list):
    user_message = {
        "role": "user",
        "content": payload,  # This is the list of dicts with type: text/image_url
    }

    # Now build the messages list correctly
    messages = [{"role": "system", "content": system_prompt}, user_message]
    print(f"sent request: {call_id}")
    completion = await openai_client_async.chat.completions.create(
        model="kimi-k2.6",
        messages=messages,
        response_format={"type": "json_object"},
        extra_body={"thinking": {"type": "disabled"}},
    )
    print(f"got request: {call_id}")
    content = json.loads(completion.choices[0].message.content)
    return call_id, content


def process_pdf_to_payload(pdf_path):
    """
    Synchronous heavy lifting: Open PDF from memory and render pages.
    """
    pdf_document = fitz.open(pdf_path)
    content_payload = [
        {
            "type": "text",
            "text": "Here is a wood structure report. Please analyze it according to the given instructions.",
        }
    ]

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        # Render page to image (DPI 200 is a good balance for LLM OCR)
        pix = page.get_pixmap(dpi=200)
        image_bytes = pix.tobytes("png")
        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        content_payload.append(
            {"type": "text", "text": f"Content from Page {page_num + 1}:"}
        )
        content_payload.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
            }
        )

    pdf_document.close()
    return content_payload
