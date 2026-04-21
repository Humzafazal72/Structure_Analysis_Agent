import io
import json
import random
from fastapi import UploadFile, Form, File
from fastapi import APIRouter, HTTPException
from sse_starlette import EventSourceResponse

from services import get_logger
from core.llm.clients import google_client_async
from services import get_graph
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

router = APIRouter()

logger = get_logger(__name__)


@router.post("/api/start_agent")
async def start_agent(structure_plan: UploadFile = File(...)):
    try:
        project_id = random.randint(0, 10000) - random.randint(0, 999)
        file_content = await structure_plan.read()
        file_obj = io.BytesIO(file_content)
        uploaded_file = await google_client_async.files.upload(
            file=file_obj,
            config={
                "mime_type": "application/pdf",
                "display_name": "user_upload.pdf",
            },
        )
        initial_state = {
                "file_uri": uploaded_file.uri,
                "file_name": uploaded_file.name,
        }
        # initial_state = {
        #     "file_uri": "https://generativelanguage.googleapis.com/v1beta/files/akzkoj95anyv",
        #     "file_name": "files/akzkoj95anyv",
        # }

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
                # Catch the graph error here and stream it to the client
                logger.error(f"Graph execution failed: {e}")
                yield {
                    "event": "error",
                    "data": json.dumps({"detail": str(e)})
                }

            finally:
                await cm.__aexit__(None, None, None)

        return EventSourceResponse(event_generator())

    except Exception as e:
        logger.critical(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong.")
