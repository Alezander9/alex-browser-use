import asyncio

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from browser_use import Agent

load_dotenv()


async def run_agent(task: str, max_steps: int = 38):
	llm = ChatAnthropic(
		model_name='claude-3-5-sonnet-20240620',
		temperature=0.0,
		timeout=100,
		stop=None,
	)
	agent = Agent(task=task, llm=llm)
	result = await agent.run(max_steps=max_steps)
	return result

if __name__ == '__main__':
	task = 'Go to https://www.google.com and search for "python" and click on the first result'
	result = asyncio.run(run_agent(task))
	print(result)