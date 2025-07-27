import logging
import os
import sqlite3
import yaml

from dotenv import load_dotenv
from pathlib import Path
from typing import Dict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from .prompt import get_system_prompt
from .state import AgentState
from .tools import reddit_tool, google_news_tool, twitter_tool, local_data_tool

load_dotenv()


class Agent:
    def __init__(self):
        self.tools = [
            reddit_tool,
            google_news_tool,
            twitter_tool,
            local_data_tool,
        ]
        self.graph = None
        self.memory = None
        self.graph_path = Path("output/agent_graph.png")
        self.conditions = self.load_conditions("categories.yaml")

        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0.2,
            max_retries=3,
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        # Wrap deep_research into a callable Tool
        self.deep_research_tool = Tool.from_function(
            func=self.deep_research_wrapper,
            name="deep_research",
            description="Conduct deep research using Reddit, Twitter, Google News, and Local Data."
        )

        self.agent = self.create_agent(self.llm)

    def load_conditions(self, filepath: str) -> Dict[str, list]:
        try:
            with open(filepath, "r") as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise RuntimeError(f"Error loading conditions from {filepath}: {e!s}")

    def categorize(self, data: Dict[str, str]) -> Dict[str, str]:
        description = data.get("description", "")
        if not description:
            raise ValueError("Missing 'description' in input JSON")

        location_categories = self.conditions["location_category"]
        road_closure_conditions = self.conditions["road_closure_conditions"]

        system_prompt = (
            "You are a helpful assistant that classifies road reports into two categories: "
            "a location and a road closure condition. "
            f"Pick exactly one location from the following list:\n{location_categories}\n\n"
            f"And exactly one road closure condition from this list:\n{road_closure_conditions}\n\n"
            "Given a description, respond with a JSON object in this format:\n"
            '{"location": "...", "condition": "..."}\n\n'
            "Respond only with the JSON. No explanation or extra text."
        )

        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=description)
        ])

        try:
            return response.content
        except Exception as e:
            raise ValueError(f"Failed to parse model response: {response.content}") from e

    def deep_research_wrapper(self, query: str) -> str:
        messages = [HumanMessage(content=query)]
        llm_with_tools = self.llm.bind_tools(self.tools)
        response = llm_with_tools.invoke(messages)
        return response.content

    def create_agent(self, llm):
        graph_builder = StateGraph(AgentState)

        def chatbot(state: AgentState):
            llm_with_tool = self.llm.bind_tools([self.deep_research_tool])
            response = llm_with_tool.invoke(state["messages"])
            return {"messages": [response]}

        # If you still want to define this for completeness
        def deep_research_node(state: AgentState):
            llm_with_tools = self.llm.bind_tools(self.tools)
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        tool_node = ToolNode(tools=self.tools)

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("deep_research", deep_research_node)
        graph_builder.add_node("tools", tool_node)

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        self.memory = InMemorySaver()
        logging.info("Successfully initialized Memory connection")

        graph = graph_builder.compile(checkpointer=self.memory)
        self.graph = graph

        with self.graph_path.open("wb") as f:
            f.write(graph.get_graph().draw_mermaid_png())

        logging.info(f"Graph visualization saved to {self.graph_path}")
        return graph

    def process_message(self, user_input: str, session_id: str | None = None) -> str:
        try:
            logging.info("=== Starting message processing ===")
            logging.info(f"Session ID: {session_id}")
            logging.info(f"Input message: {user_input}")

            config = {
                "configurable": {
                    "thread_id": session_id,
                },
            }

            logging.info(f"Using thread ID: {config['configurable']['thread_id']}")
            logging.info("Invoking agent with message")

            events = self.agent.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input or "ignore this message"),
                        SystemMessage(content=get_system_prompt()),
                    ],
                    "llm": self.llm,
                },
                config,
                stream_mode="values",
            )

            for event in events:
                last_message = event["messages"][-1]

            logging.info("Agent response received successfully")
            logging.info(f"Response content: {last_message.content[:100]}...")
            return last_message.content

        except Exception as e:
            logging.error(f"Unexpected error in process_message: {e!s}", exc_info=True)
            raise
