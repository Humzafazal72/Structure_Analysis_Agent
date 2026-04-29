import os
from google.genai import Client
from openai import AsyncOpenAI

google_client_async = Client().aio
openai_client_async = AsyncOpenAI(api_key=os.environ["KIMI_API_KEY"],
                                  base_url="https://api.moonshot.ai/v1")
