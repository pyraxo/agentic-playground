from typing import Annotated

from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from app.config import get_settings
from app.models import Agent
from app.schemas.message import Message

settings = get_settings()


class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_tools() -> list[BaseTool]:
    arxiv_tool = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())
    pubmed_tool = PubmedQueryRun()
    wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    duckduckgo_tool = DuckDuckGoSearchRun()

    return [arxiv_tool, pubmed_tool, wikipedia_tool, duckduckgo_tool]


llm = ChatOpenAI(
    model="gpt-4o-mini", temperature=0, api_key=settings.openai_api_key
).bind_tools(build_tools())


def agent_node(state: State) -> State:
    return {"messages": [llm.invoke(state["messages"])]}


def build_workflow():
    workflow = StateGraph(State)

    workflow.add_node("agent", agent_node)

    tool_node = ToolNode(build_tools())
    workflow.add_node("tools", tool_node)

    workflow.add_conditional_edges("agent", tools_condition, ["tools", END])

    workflow.add_edge("tools", "agent")
    workflow.set_entry_point("agent")

    return workflow.compile()


graph = build_workflow()


async def invoke_agent(agent: Agent, message: Message) -> list[dict]:
    """Invoke an agent."""
    knowledge_base = ""
    if len(agent.files) > 0:
        files = "\n".join([file.text for file in agent.files])
        knowledge_base = f"Your knowledge base includes the following:\n{files}\n\nUse this context to provide answers. Use external tools only if the information provided is insufficient."
    if not agent.prompt:
        prompt = f"You are a research assistant. Your task is to answer the user's question as accurately as possible, with detailed explanations and reasoning.\n{knowledge_base}"
    else:
        prompt = f"{agent.prompt}\n{knowledge_base}"
    messages = [
        SystemMessage(
            content=prompt,
        ),
        HumanMessage(content=message.message),
    ]
    result = await graph.ainvoke({"messages": messages})
    return result
