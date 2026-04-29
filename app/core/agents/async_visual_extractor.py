import asyncio
from google.genai import types
from google.genai.errors import ClientError

from core.schema import (
    AgentState,
    ShearWallData,
    RoofSystemData,
    WallSystemData,
    PostData,
    FloorSystemData,
    FootingSystemData,
)
from core.llm.prompts import (
    SYS_PROMPT_FLOOR,
    SYS_PROMPT_FOOTING,
    SYS_PROMPT_POST,
    SYS_PROMPT_ROOF,
    SYS_PROMPT_SHEAR_WALL,
    SYS_PROMPT_WALL,
)
from core.llm.clients import openai_client_async
from core.utils import fetch_with_id, fetch_with_id_kimi
from services import get_logger


logger = get_logger(__name__)


async def visual_extractor(agent_state: AgentState):
    #try:
        floor_config = types.GenerateContentConfig(
            system_instruction=SYS_PROMPT_FLOOR,
            response_schema=FloorSystemData,
            response_mime_type="application/json",
        )
        footing_config = types.GenerateContentConfig(
            system_instruction=SYS_PROMPT_FOOTING,
            response_schema=FootingSystemData,
            response_mime_type="application/json",
        )
        post_config = types.GenerateContentConfig(
            system_instruction=SYS_PROMPT_POST,
            response_schema=PostData,
            response_mime_type="application/json",
        )
        roof_config = types.GenerateContentConfig(
            system_instruction=SYS_PROMPT_ROOF,
            response_schema=RoofSystemData,
            response_mime_type="application/json",
        )
        shear_wall_config = types.GenerateContentConfig(
            system_instruction=SYS_PROMPT_SHEAR_WALL,
            response_schema=ShearWallData,
            response_mime_type="application/json",
        )
        wall_config = types.GenerateContentConfig(
            system_instruction=SYS_PROMPT_WALL,
            response_schema=WallSystemData,
            response_mime_type="application/json",
        )

        file_uri = agent_state.file_uri
        configs = [
            ("floor", floor_config),
            ("footing", footing_config),
            ("post", post_config),
            ("roof", roof_config),
            ("shear_wall", shear_wall_config),
            ("wall", wall_config)
        ]

        tasks = []

        # Launch tasks with a slight stagger to prevent the 400 error
        for call_id, config in configs:
            tasks.append(fetch_with_id(call_id=call_id, config=config, file_uri=file_uri))
            await asyncio.sleep(1) # <--- Critical: Give the backend 1 second to breathe

        parsed_data = {}

        for task in asyncio.as_completed(tasks):
            call_id, data = await task
            parsed_data[call_id] = data
            logger.info(f"Finished {call_id}")

        return {
            "roof_system": parsed_data["roof"].model_dump(),
            "floor_system": parsed_data["floor"].model_dump(),
            "footing": parsed_data["footing"].model_dump(),
            "post": parsed_data["post"].model_dump(),
            "wall": parsed_data["wall"].model_dump(),
            "shear_wall": parsed_data["shear_wall"].model_dump(),
        }
    
    # except ClientError as e:
    #     logger.error(f"Google API Client Error: {e.message}")
    #     raise Exception("AI Quota exceeded or invalid request.")

    # except Exception as e:
    #     logger.critical("Error: ", e)
    #     raise Exception("Something went Wrong while extracting data from document")

async def visual_extractor_kimi(agent_state: AgentState):
    #try:
        floor_config = SYS_PROMPT_FLOOR
        footing_config = SYS_PROMPT_FOOTING,
        post_config = SYS_PROMPT_POST,
        roof_config = SYS_PROMPT_ROOF,
        shear_wall_config = SYS_PROMPT_SHEAR_WALL,
        wall_config = SYS_PROMPT_WALL,

        configs = [
            ("floor", floor_config),
            ("footing", footing_config),
            ("post", post_config),
            ("roof", roof_config),
            ("shear_wall", shear_wall_config),
            ("wall", wall_config)
        ]

        tasks = []
        file_content = openai_client_async.files.content(file_id=agent_state.file_id).text

        # Launch tasks with a slight stagger to prevent the 400 error
        for call_id, config in configs:
            tasks.append(fetch_with_id_kimi(call_id=call_id, config=config, file_content=file_content))
            await asyncio.sleep(1)

        parsed_data = {}

        for task in asyncio.as_completed(tasks):
            call_id, data = await task
            parsed_data[call_id] = data
            logger.info(f"Finished {call_id}")

        return {
            "roof_system": parsed_data["roof"],
            "floor_system": parsed_data["floor"],
            "footing": parsed_data["footing"],
            "post": parsed_data["post"],
            "wall": parsed_data["wall"],
            "shear_wall": parsed_data["shear_wall"],
        }
    
    # except ClientError as e:
    #     logger.error(f"Google API Client Error: {e.message}")
    #     raise Exception("AI Quota exceeded or invalid request.")

    # except Exception as e:
    #     logger.critical("Error: ", e)
    #     raise Exception("Something went Wrong while extracting data from document")
