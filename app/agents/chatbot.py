import os
from typing import Annotated

from dotenv import load_dotenv
from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

load_dotenv()


class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_tools() -> list[BaseTool]:
    arxiv_tool = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())
    pubmed_tool = PubmedQueryRun()
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    duckduckgo_tool = DuckDuckGoSearchRun()

    return [arxiv_tool, pubmed_tool, wikipedia_tool, duckduckgo_tool]


llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
).bind_tools(build_tools())


def agent(state: State) -> State:
    return {"messages": [llm.invoke(state["messages"])]}


def build_workflow():
    workflow = StateGraph(State)

    workflow.add_node("agent", agent)

    tool_node = ToolNode(build_tools())
    workflow.add_node("tools", tool_node)

    workflow.add_conditional_edges("agent", tools_condition, ["tools", END])

    workflow.add_edge("tools", "agent")
    workflow.set_entry_point("agent")

    return workflow.compile()


graph = build_workflow()
