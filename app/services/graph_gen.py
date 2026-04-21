import os
from contextlib import asynccontextmanager
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from core.workflow import workflow 

async def get_graph():
    """Initiate the langgraph graph and create the postgres checkpointer"""
    postgre_conn_string = os.getenv("SUPABASE_DB_URL")
    
    # 1. Create a custom context manager to match your endpoint's lifecycle
    @asynccontextmanager
    async def custom_pool_manager():
        # 2. Build the pool manually to forcefully inject the kwargs
        pool = AsyncConnectionPool(
            conninfo=postgre_conn_string,
            max_size=20, # Adjust based on your expected traffic
            kwargs={
                "autocommit": True,
                "prepare_threshold": None # The magic fix for PgBouncer/Supabase
            }
        )
        try:
            # 3. Hand the custom pool directly to the Saver
            saver = AsyncPostgresSaver(pool)
            yield saver
        finally:
            # Safely close the pool when the API stream disconnects
            await pool.close()

    # 4. Use the custom manager exactly like you used the old 'cm'
    cm = custom_pool_manager()
    checkpointer = await cm.__aenter__()
    
    # Set up tables if they don't exist
    await checkpointer.setup()
    
    # Compile the graph
    graph = workflow.compile(checkpointer=checkpointer)
    
    return graph, cm