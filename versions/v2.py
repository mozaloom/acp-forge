from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server

from crewai import Crew, Task, Agent, LLM
from crewai_tools import RagTool
import os
# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings('ignore')


server = Server()
llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY"),
    max_tokens=2048,
    temperature=0.1,
    top_p=0.9,
    frequency_penalty=0.0,
    presence_penalty=0.0,
)

config = {
    "llm": {
        "provider": "google",
        "config": {
            "model": "gemini/gemini-1.5-flash",
            "api_key": os.getenv("GEMINI_API_KEY"),
            "max_tokens": 1024
        }
    },
    "embedding_model": {
        "provider": "google",
        "config": {
            "model": "models/text-embedding-004"
        }
    },

}

rag_tool = RagTool(
    config=config,
    chunk_size=1200,
    chunk_overlap=200
)

rag_tool.add("gold-hospital-and-premium-extras.pdf")

@server.agent()
async def policy_agent(input: Message) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    Agent to handle insurance policy queries using the RAG tool.
    """
    insurance_agent = Agent(
        role="Senior Insurance Coverage Assistant",
        goal="Use the RAG tool to search insurance policy documents and provide accurate answers",
        backstory="""You are an expert insurance agent with access to a RAG tool that can search policy documents. 
        ALWAYS use the RAG tool first to search for information before providing any answer. 
        You have access to a knowledge base tool - use it to find relevant policy information.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[rag_tool],
        max_retry_limit=5,
        step_callback=lambda step: print(f"Agent step: {step}")
    )

    task1 = Task(
        description=input[0].parts[0].content,
        expected_output="A detailed answer about the waiting period for rehabilitation services based on the policy document, including specific time periods found",
        agent=insurance_agent
    )

    crew = Crew(agents=[insurance_agent], tasks=[task1], verbose=True)
    task_output = await crew.kickoff()
    yield Message(
        parts=[MessagePart(
            content=str(task_output))])
    
if __name__ == "__main__":
    server.run(port=8001)



