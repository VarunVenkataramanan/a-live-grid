import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command

from app.agent.prompt import get_system_prompt
from app.agent.state import AgentState
from app.agent.tools import google_news_tool, local_data_tool, reddit_tool, twitter_tool

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

		self.agent = self.create_agent(self.llm)

	def load_conditions(self, filepath: str) -> dict[str, list]:
		try:
			with open(filepath) as file:
				return yaml.safe_load(file)
		except Exception as e:
			raise RuntimeError from e(f"Error loading conditions from {filepath}: {e!s}")

	def categorize(self, description: str) -> list[str, str]:
		"""
		Classifies a description into one of the known locations and road closure conditions.
		"""
		if not description:
			raise ValueError("Missing 'description' in input JSON")

		location_categories = self.conditions["location_category"]
		road_closure_conditions = self.conditions["road_closure_conditions"]

		system_prompt = (
			"You are a helpful assistant that classifies road reports into two categories: "
			"a location and a road closure condition. "
			f"Pick exactly one location from the following list:\n{location_categories}\n\n"
			f"And exactly one road closure condition from this list:\n{road_closure_conditions}\n\n"
			"Given a description, respond with a string object"
			"It should be only of the format '<location>, <condition>'"
		)

		response = self.llm.invoke(
			[
				SystemMessage(content=system_prompt),
				HumanMessage(content=description),
			],
		)

		location = response.content.split(",")[0].strip()
		condition = response.content.split(",")[1].strip()

		try:
			return location, condition
		except Exception as e:
			raise ValueError(f"Failed to parse model response: {response.content}") from e

	def create_agent(self, llm):
		tools = self.tools
		graph_builder = StateGraph(AgentState)

		def chatbot(state: AgentState):
			# Sample for get_db_manager() and Command usage
			# verified = get_db_manager().verify_customer(variable)
			# if not verified:
			# 	return Command(goto="verify_customer")
			llm_with_tools = llm.bind_tools(deep_research)
			response = llm_with_tools.invoke(state["messages"])
			return {"messages": [response]}

		def deep_research(state: AgentState):
			# Sample for get_db_manager() and Command usage
			# verified = get_db_manager().verify_customer(variable)
			# if not verified:
			# 	return Command(goto="verify_customer")
			llm_with_tools = llm.bind_tools(tools)
			return {"messages": [llm_with_tools.invoke(state["messages"])]}

		# def deep_research_node(state: AgentState):

		tool_node = ToolNode(tools=tools)
		graph_builder.add_node("chatbot", chatbot)
		# deep research should be a node, cuz i need data, which comes from tools.
		graph_builder.add_node("tools", tool_node)
		graph_builder.add_edge(START, "chatbot")
		graph_builder.add_conditional_edges(
			"chatbot",
			tools_condition,
		)
		graph_builder.add_edge("tools", "chatbot")

		# memory = SqliteSaver(conn)
		memory = InMemorySaver()
		self.memory = memory
		logging.info("Successfully initialized Memory  connection")
		graph = graph_builder.compile(checkpointer=memory)
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
						HumanMessage(content=user_input if user_input else "ignore this message. Dont reply to this message"),
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
