import os
from typing import Annotated

from langchain.agents import load_tools
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict


class State(TypedDict):
    messages: Annotated[list, add_messages]


arxiv_tool = load_tools(["arxiv"])
pubmed_tool = PubmedQueryRun()
wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
duckduckgo_tool = DuckDuckGoSearchRun()
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
).bind_tools([arxiv_tool, pubmed_tool, wikipedia_tool, duckduckgo_tool])


workflow = StateGraph(State)


def agent(state: State) -> State:
    return {"messages": [llm.invoke(state["messages"])]}


workflow.add_node("agent", agent)

tool_node = ToolNode([arxiv_tool, pubmed_tool, wikipedia_tool, duckduckgo_tool])
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges("agent", tools_condition, ["tools", END])

workflow.add_edge("tools", "agent")
workflow.set_entry_point("agent")

graph = workflow.compile()
