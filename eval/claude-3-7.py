from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from browser_use import Agent

import asyncio

load_dotenv()


async def run_agent(task: str, max_steps: int = 15):
	llm = ChatAnthropic(
		model_name='claude-3-7-sonnet-latest',
		temperature=0.0,
		timeout=100,
		stop=None,
	)
	agent = Agent(task=task, llm=llm, use_vision=False, remove_empty_elements=True)
	result = await agent.run(max_steps=max_steps)
	return result

if __name__ == '__main__':
	task = """Find information about the valuation of Meta on yahoo finance"""
	result = asyncio.run(run_agent(task))
	print(result)
