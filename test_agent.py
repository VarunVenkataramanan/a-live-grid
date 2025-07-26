from app.agent.agent import Agent


def run_categorize_test():
	"""
	A simple function to test the categorize method of the Agent class.
	"""
	agent = Agent()
	description = "Heavy rainfall has caused severe water logging on Airport Road near the Hebbal junction. The underpass is completely flooded and traffic is being diverted. Avoid this area until the water recedes."

	location, condition = agent.categorize(description)

	print(f"Categorization response: {location},{condition}")
	print(type(location), type(condition))


def run_chat_test():
	"""
	A simple function to test the process_message method of the Agent class.
	"""
	agent = Agent()
	user_message = "Hello, what is the weather like today?"
	session_id = "test_session_123"  # Use a consistent session ID for testing

	chat_response = agent.process_message(user_message, session_id)

	print(f"Chat response: {chat_response}")


if __name__ == "__main__":
	print("\n--- Running Chat Test ---")
	run_chat_test()
