from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, VisitWebpageTool

server = Server()

model = LiteLLMModel(
    model_id="gemini/gemini-1.5-flash",
    max_tokens=2048
)

@server.agent()
async def health_agent(input: Message) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    this is a code agent which supports the hospital to handle health-related questions for patients. Current or prospective patients can ask questions about their health, and the agent will use web search and webpage visits to find answers.
    """
    # Initialize the CodeAgent with the model and tools
    code_agent = CodeAgent(
        model=model,
        tools=[
            DuckDuckGoSearchTool(),
            VisitWebpageTool()
        ]
    )
    
    # Use the CodeAgent to process the input
    response = await code_agent.run(input[0].parts[0].content)
    
    yield Message(
        parts=[MessagePart(content=str(response))]
    )

if __name__ == "__main__":
    server.run(port=8000)
    # Note: Debug mode is optional; you can remove it if not needed.