from acp_sdk.client import Client
import asyncio
from colorama import Fore

async def example() -> None:
    try:
        async with Client(base_url="http://localhost:8001") as client:
            run = await client.run_sync(
                agent="policy_agent", input="What is the waiting period for rehabilitation?"
            )
            
            # Debug: Print the full response structure
            print(f"Run object: {run}")
            print(f"Run output: {run.output}")
            print(f"Run output type: {type(run.output)}")
            
            # Check if output exists and has content
            if run.output and len(run.output) > 0:
                if hasattr(run.output[0], 'parts') and len(run.output[0].parts) > 0:
                    print(Fore.YELLOW + run.output[0].parts[0].content + Fore.RESET)
                else:
                    print(Fore.RED + f"No parts found in output: {run.output[0]}" + Fore.RESET)
            else:
                print(Fore.RED + "No output received from agent" + Fore.RESET)
                
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Fore.RESET)
        print(Fore.RED + "Make sure the server is running with: python rag.py" + Fore.RESET)


if __name__ == "__main__":
    asyncio.run(example())
    print(Fore.YELLOW + "Run completed successfully." + Fore.RESET)
    print("You can now use the agent to ask questions about the insurance policy.")
    print("Example: 'What is the waiting period for rehabilitation services?'")