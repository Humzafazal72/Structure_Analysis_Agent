import os
import json
import random
import asyncio
import tempfile
from fastapi import UploadFile, Form, File
from fastapi import APIRouter, HTTPException
from sse_starlette import EventSourceResponse

from services import get_logger
from services import get_graph
from core.llm.clients import google_client_async, openai_client_async

router = APIRouter()

logger = get_logger(__name__)


#  ---------------------------- v1 with gemini
@router.post("/api/v1/start_agent")
async def start_agent(structure_plan: UploadFile = File(...)):
    project_id = random.randint(0, 10000) - random.randint(0, 999)
    
    # 1. Read the incoming file content
    file_content = await structure_plan.read()
    
    # 2. Write to a temporary physical file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name

    try:
        uploaded_file = await google_client_async.files.upload(
            file=temp_file_path,
            config={
                "mime_type": "application/pdf",
                "display_name": "user_upload.pdf",
            },
        )
        # 3. Pass the physical file path to the SDK
        file_info = await google_client_async.files.get(name=uploaded_file.name)
        
        # Keep checking the state every 2 seconds
        while file_info.state.name == "PROCESSING":
            logger.info(f"File {uploaded_file.name} is processing. Waiting 2 seconds...")
            await asyncio.sleep(2)
            file_info = await google_client_async.files.get(name=uploaded_file.name)
            
        # If the backend failed to parse the PDF, abort
        if file_info.state.name == "FAILED":
            raise HTTPException(status_code=400, detail="Google API failed to process the PDF.")
        # ---------------------------------------------------------

        # Now it is safe to pass the URI to the agent
        initial_state = {
            "file_uri": uploaded_file.uri,
            "file_name": uploaded_file.name,
        }

        graph_app, cm = await get_graph()
        config = {"configurable": {"thread_id": f"{project_id}"}}

        async def event_generator():
            try:
                async for event in graph_app.astream(
                    input=initial_state, config=config
                ):
                    for node_name, node_data in event.items():
                        serializable_data = {}
                        for key, value in node_data.items():
                            if hasattr(value, "model_dump"):
                                serializable_data[key] = value.model_dump()
                            else:
                                serializable_data[key] = value
                        yield {
                            "event": node_name,
                            "data": json.dumps(serializable_data),
                        }
            
            except Exception as e:
                logger.error(f"Graph execution failed: {e}")
                yield {
                    "event": "error",
                    "data": json.dumps({"detail": str(e)})
                }

            finally:
                await cm.__aexit__(None, None, None)

        return EventSourceResponse(event_generator())

    finally:
        # 4. Ensure the temp file is cleaned up no matter what happens
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# ----------------------------------------v2 with kimi
@router.post("/api/v2/start_agent")
async def start_agent(structure_plan: UploadFile = File(...)):
    try:
        project_id = random.randint(0, 10000) - random.randint(0, 999)

        # 1. Read the incoming file content
        file_content = await structure_plan.read()

        # 2. Write to a temporary physical file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        file_object = await openai_client_async.files.create(file=temp_file_path, purpose="file-extract")

    
        initial_state = {
            "file_id": file_object.id
        }

        graph_app, cm = await get_graph()
        config = {"configurable": {"thread_id": f"{project_id}"}}

        async def event_generator():
            try:
                async for event in graph_app.astream(
                    input=initial_state, config=config
                ):
                    for node_name, node_data in event.items():
                        serializable_data = {}
                        for key, value in node_data.items():
                            if hasattr(value, "model_dump"):
                                serializable_data[key] = value.model_dump()
                            else:
                                serializable_data[key] = value
                        yield {
                            "event": node_name,
                            "data": json.dumps(serializable_data),
                        }
            
            except Exception as e:
                logger.error(f"Graph execution failed: {e}")
                yield {
                    "event": "error",
                    "data": json.dumps({"detail": str(e)})
                }

            finally:
                await cm.__aexit__(None, None, None)

        return EventSourceResponse(event_generator())

    finally:
        # 4. Ensure the temp file is cleaned up no matter what happens
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)