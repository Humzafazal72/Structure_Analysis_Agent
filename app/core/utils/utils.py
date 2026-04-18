from google.genai import types
from core.llm.clients import google_client_async

async def fetch_with_id(call_id: str, file_uri: str, config: types.GenerateContentConfig):
    response = await google_client_async.models.generate_content(
        model='gemini-2.0-flash',
        config=config,
        contents=[
            types.Part.from_uri(
                file_uri=file_uri,
                mime_type='application/pdf'
            ),
            "Analyze the given structural plan based on the provided instructions"
        ]
    )
    return call_id, response.parsed