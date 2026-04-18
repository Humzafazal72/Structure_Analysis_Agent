from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from services import get_logger
from routes.agent import start_agent

logger = get_logger(__name__)
app = FastAPI()

app.include_router(start_agent.router, prefix="", tags=["Agent"])


@app.get("/health")
async def health():
    try:
        return JSONResponse(content="App running...", status_code=200)
    except Exception as e:
        logger.critical("Error: ", e)
        raise HTTPException(status_code=500, detail="Something went wrong")