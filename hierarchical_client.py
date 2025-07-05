import asyncio 
import nest_asyncio
from acp_sdk.client import Client
from smolagents import LiteLLMModel
from fastacp import AgentCollection, ACPCallingAgent
from colorama import Fore

nest_asyncio.apply()

model = LiteLLMModel(
    model_id="gemini/gemini-1.5-flash"
)

async def run_hospital_workflow() -> None:
    async with Client(base_url="http://localhost:8001") as insurer, Client(base_url="http://localhost:8000") as hospital:
        agent_collection = await AgentCollection.from_acp(insurer, hospital)
        acp_agents = {agent.name: {'agent': agent, 'client': client} for client, agent in agent_collection.agents}

        print(acp_agents)

        acpagent = ACPCallingAgent(acp_agents=acp_agents, model=model)

        result = await acpagent.run("do i need rehabilitation after a shoulder reconstruction and what is the waiting period from my insurance?")
        print(Fore.YELLOW + f"Final result: {result}" + Fore.RESET)

if __name__ == "__main__":
    asyncio.run(run_hospital_workflow())