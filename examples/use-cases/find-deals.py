import asyncio
import os
import sys

from pydantic import BaseModel

# Install the browser-use package with import browser_use, in this case we are inside the browser-use repo so we will import from path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Load our API keys
from dotenv import load_dotenv

load_dotenv()

# Check if the API key is set
if not os.getenv('OPENAI_API_KEY'):
	raise ValueError('OPENAI_API_KEY is not set. Please add it to your environment variables.')

# Import the Agent and Controller classes
from browser_use import Agent
from browser_use.browser import BrowserProfile, BrowserSession

# Import the ChatOpenAI class
from browser_use.llm import ChatOpenAI
from browser_use.llm.messages import (
	SystemMessage,
	UserMessage,
)

# Create a judge model that will analyze deals and decide whether to buy them.
judge_model = ChatOpenAI(model='gpt-4.1-mini')


class JudgeResult(BaseModel):
	judgement: str  # 1 sentence summary


# test the judge model
def test_judge_model():
	system_prompt = 'You are a judge that will analyze deals and decide whether to buy them.'
	user_prompt = 'What is the best deal on a laptop?'

	messages = [
		SystemMessage(content=system_prompt),
		UserMessage(content=user_prompt),
	]
	output = judge_model.ainvoke(messages, output_format=JudgeResult)

	print(output)


# Example placeholder credit card info
credit_card_info = {'name': 'John Doe', 'number': '1234567890123456', 'expiry': '12/2025', 'cvv': '123'}

# Example placeholder google account info
google_account_info = {'email': 'demojohn136@gmail.com', 'password': 'hQcx2gPvXr6CL7znm7QT'}


async def main():
	task = """Go to temu and filter by "local warehouse", then scroll and click on items that relate to the following categories: technology, games, sports, household gadgets, furtniture, dorm room decor, funny t shirts, plushies, gear, robotics. Avoid things that are boring, fashion, cosmetics, or anything sexual or controversial. Keep track of how many items you have visited and stop at 15. Keep track of what categories you have hit and try not to repeat categories, and try to achieve all categories. Use the search bar if  you cannot find a category from recommendations"""

	browser_profile = BrowserProfile(headless=False, user_data_dir='./shopping_profile')
	browser_session = BrowserSession(browser_profile=browser_profile)

	# Navigate to temu
	await browser_session.navigate('https://www.temu.com/')

	model = ChatOpenAI(model='gpt-4.1-mini')
	agent = Agent(
		task=task,
		llm=model,
		browser_session=browser_session,
	)

	history = await agent.run()

	# # Initialize an empty agent state, we will be modifying this state as we go
	# agent_state = AgentState()

	# for i in range(30):
	#     # By reinitializng the agent every step with injected_agent_state, we can insert things into the state between steps
	#     agent = Agent(
	#         task=task,
	#         llm=ChatOpenAI(model='gpt-4.1-mini'),
	#         browser_session=browser_session,
	#         injected_agent_state=agent_state,
	#     )

	#     done, valid = await agent.take_step()
	#     print(f'Step {i}: Done: {done}, valid: {valid}')

	#     # Escape loop if agent marks self as done
	#     if done and valid:
	#         break

	# agent_state.history.history = []

	# # Get feedback on agent state
	# # pseudocode
	# feedback = "IMPORTANT ADDITIONAL USER TASK: Open the wikipedia page for types of batteries and read the page"

	# # Add feedback into the agent message manager
	# agent.message_manager._add_message_with_type(
	#         UserMessage(content=feedback),
	#         'consistent'  # This message persists across steps
	#     )

	# break

	# Close the browser
	# print("Task Done, closing browser")
	# await browser_session.close()


if __name__ == '__main__':
	asyncio.run(main())
