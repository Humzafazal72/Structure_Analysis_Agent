from langgraph.graph import StateGraph, START, END

from core.schema import AgentState
from core.agents import visual_extractor, visual_extractor_kimi

workflow = StateGraph(AgentState)

# Nodes
# workflow.add_node("visual_extractor",visual_extractor)
workflow.add_node("visual_extractor", visual_extractor)

# Edges
workflow.add_edge(START, "visual_extractor")
workflow.add_edge("visual_extractor", END)