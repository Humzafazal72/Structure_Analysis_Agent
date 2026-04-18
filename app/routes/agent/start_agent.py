import io
import random
from fastapi import UploadFile, Form, File
from fastapi import APIRouter, HTTPException
from sse_starlette import EventSourceResponse

from services import get_logger
from core.workflow import workflow
from core.llm.clients import google_client_async
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

router = APIRouter()

logger = get_logger(__name__)

@router.post("/api/start_agent")
async def start_agent(structure_plan: UploadFile = File(...), user_id: str = Form(...)):
    try:
        project_id = random.randint(0, 10000) - random.randint(0, 999)
        file_content = await structure_plan.read()
        file_obj = io.BytesIO(file_content)

        async def event_generator():
            async with AsyncSqliteSaver.from_conn_string("storage/checkpoints.db") as saver:
                app = workflow.compile(checkpointer=saver)

                config = {"configurable": {"thread_id": f"{user_id}_{project_id}"}}

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

                async for event in app.astream(input=initial_state, config=config):
                    for node_name, node_data in event.items():
                        yield ({"event": node_name, "data": ""}) #json.dumps(node_data)

        return EventSourceResponse(event_generator())

    except Exception as e:
        logger.critical("Error: ")
        raise HTTPException(status_code=500, detail="Something went wrong.")