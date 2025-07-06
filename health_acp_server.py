from collections.abc import AsyncGenerator
from acp_sdk.models import Message, MessagePart
from acp_sdk.server import RunYield, RunYieldResume, Server
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, VisitWebpageTool, ToolCallingAgent, ToolCollection
from mcp import StdioServerParameters

server = Server()

model = LiteLLMModel(
    model_id="gemini/gemini-1.5-flash",
    max_tokens=2048
)

server_parameters = StdioServerParameters(
    command="python",
    args=["mcpserver.py"],
    env=None
)


@server.agent()
async def doctor_agent(input: Message) -> AsyncGenerator[RunYield, RunYieldResume]:
    """ This is a Doctor Agent which helps users find doctors near them"""
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        agent = ToolCallingAgent(tools=[*tool_collection.tools], model=model)
        prompt = input[0].parts[0].content
        response = agent.run(prompt)
        yield Message(
            parts=[MessagePart(content=str(response))]
        )



@server.agent()
async def health_agent(input: Message) -> AsyncGenerator[RunYield, RunYieldResume]:
    """
    A health information agent that searches for general medical information to help patients understand common procedures and treatments. 
    
    This agent should:
    1. Always attempt to search for reliable medical information first
    2. Provide educational information from reputable sources
    3. Include appropriate medical disclaimers
    4. Encourage consultation with healthcare professionals for personalized advice
    
    The agent should be helpful in providing general medical education while being clear about the limitations.
    """
    # Create a more detailed prompt to guide the agent's behavior
    enhanced_query = f"""
    Please search for reliable medical information about: {input[0].parts[0].content}
    
    Instructions:
    1. Use web_search to find information from reputable medical sources (Mayo Clinic, WebMD, NHS, medical journals)
    2. If search fails due to rate limits, try alternative search terms
    3. Provide educational information about the medical topic
    4. Always include a disclaimer that this is general information and patients should consult their healthcare provider
    5. Be helpful and informative while maintaining appropriate medical boundaries
    
    Do NOT immediately decline to help - attempt to find and provide general medical education first.
    """
    
    # Initialize the CodeAgent with the model and tools
    code_agent = CodeAgent(
        model=model,
        tools=[
            DuckDuckGoSearchTool(),
            VisitWebpageTool()
        ]
    )
    
    # Use the CodeAgent to process the enhanced query
    response = code_agent.run(enhanced_query)
    
    yield Message(
        parts=[MessagePart(content=str(response))]
    )

if __name__ == "__main__":
    server.run(port=8000)
    # Note: Debug mode is optional; you can remove it if not needed.