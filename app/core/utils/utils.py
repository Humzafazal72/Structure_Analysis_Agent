import json
from google.genai import types
from core.llm.clients import google_client_async, openai_client_async


async def fetch_with_id(
    call_id: str,
    config: types.GenerateContentConfig,
    file_uri: str,
):
    response = await google_client_async.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        config=config,
        contents=[
            types.Part.from_uri(file_uri=file_uri, mime_type="application/pdf"),
            "Analyze the given structural plan based on the provided instructions",
        ],
    )
    return call_id, response.parsed


async def fetch_with_id_kimi(call_id: str, system_prompt: str, file_content: str):
    completion = await openai_client_async.chat.completions.create(
        model="kimi-k2.6",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": file_content,
            },
            {
                "role": "user",
                "content": "Analyze the given structural plan based on the provided system instructions",
            },
        ],
        response_format={
            "type": "json_object"
        },
    )

    content = json.loads(completion.choices[0].message.content)
    return call_id, content
