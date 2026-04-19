import os
from core.workflow import workflow
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async def get_graph():
    """initiate the langgraph graph and create the sqlite checkpointer"""
    postgre_conn_string = os.getenv("SUPABASE_DB_URL")
    cm = AsyncPostgresSaver.from_conn_string(postgre_conn_string)
    checkpointer = await cm.__aenter__()
    await checkpointer.setup()
    graph = workflow.compile(checkpointer=checkpointer)
    return graph, cm