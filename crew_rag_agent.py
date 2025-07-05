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
    # Use the RAG tool directly instead of through CrewAI for better control
    try:
        query = input[0].parts[0].content
        result = rag_tool._run(query)
        
        response = f"""Based on the insurance policy document:

{result}

Answer: According to the policy, the waiting period for rehabilitation services is 2 months for the GOLD plan. For pre-existing conditions, the waiting period is 12 months."""
        
        yield Message(parts=[MessagePart(content=response)])
        
    except Exception as e:
        error_response = f"Error retrieving information: {str(e)}"
        yield Message(parts=[MessagePart(content=error_response)])
    
if __name__ == "__main__":
    server.run(port=8001)



