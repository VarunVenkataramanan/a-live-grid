import logging
import os
import yaml
from typing import Dict, List

from dotenv import load_dotenv
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

load_dotenv()


class Agent:
    def __init__(self):
        self.conditions = self.load_conditions("categories.yaml")
        
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",  # Using a more reliable model
            temperature=0.2,
            max_retries=3,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        
        # Simple tools for basic functionality
        self.tools = [
            Tool.from_function(
                func=self.local_data_search,
                name="local_data_search",
                description="Search local data and posts for relevant information"
            ),
            Tool.from_function(
                func=self.general_search,
                name="general_search", 
                description="Search for general information on a topic"
            )
        ]

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

        def tools_node(state: AgentState):
            # Simple tools node that uses the tools directly
            llm_with_tools = self.llm.bind_tools(self.tools)
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_node("deep_research", deep_research_node)
        graph_builder.add_node("tools", tools_node)

        graph_builder.set_entry_point("chatbot")
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