import asyncio
from google.genai import types

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
from core.utils import fetch_with_id
from services import get_logger


logger = get_logger(__name__)


async def visual_extractor(agent_state: AgentState):
    try:
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

        file_uri = agent_state["file_uri"]
        tasks = [
            fetch_with_id(call_id="floor", config=floor_config, file_uri=file_uri),
            fetch_with_id(call_id="footing", config=footing_config, file_uri=file_uri),
            fetch_with_id(call_id="post", config=post_config, file_uri=file_uri),
            fetch_with_id(call_id="roof", config=roof_config, file_uri=file_uri),
            fetch_with_id(call_id="shear_wall", config=shear_wall_config, file_uri=file_uri),
            fetch_with_id(call_id="wall", config=wall_config, file_uri=file_uri),
        ]

        print("came here")
        parsed_data = {}
        for task in asyncio.as_completed(tasks):
            call_id, data = await task
            parsed_data[f"{call_id}"] = data
            logger.info(f"Finished {call_id}")

        return {
            "roof_system": parsed_data["roof"],
            "floor_system": parsed_data["floor"],
            "footing": parsed_data["footing"],
            "post": parsed_data["post"],
            "wall": parsed_data["wall"],
            "shear_wall": parsed_data["shear_wall"],
        }

    except Exception as e:
        logger.critical("Error: ", e)
        raise Exception("Something went Wrong while extracting data from document")
