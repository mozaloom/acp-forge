from acp_sdk.client import Client
import asyncio
from colorama import Fore

async def run_hospital_workflow() -> None:
    try:
        async with Client(base_url="http://localhost:8001") as insurer, Client(base_url="http://localhost:8000") as hospital:
            # Step 1: Ask hospital agent about rehabilitation
            print(Fore.CYAN + "Asking hospital agent about rehabilitation..." + Fore.RESET)
            run1 = await hospital.run_sync(
                agent="health_agent",
                input="Do I need rehabilitation after a shoulder reconstruction surgery?"
            )
            
            # Debug: Check response structure
            print(f"Hospital response type: {type(run1)}")
            print(f"Hospital response: {run1}")
            
            # Handle hospital response
            if hasattr(run1, 'output') and run1.output and len(run1.output) > 0:
                if hasattr(run1.output[0], 'parts') and len(run1.output[0].parts) > 0:
                    content = run1.output[0].parts[0].content
                    print(Fore.LIGHTMAGENTA_EX + f"Hospital Agent: {content}" + Fore.RESET)
                else:
                    print(Fore.RED + f"Unexpected hospital response structure: {run1.output}" + Fore.RESET)
                    content = "Rehabilitation is typically needed after shoulder reconstruction surgery."
            else:
                print(Fore.RED + "No output from hospital agent, using fallback" + Fore.RESET)
                content = "Rehabilitation is typically needed after shoulder reconstruction surgery."

            # Step 2: Ask insurance agent about waiting periods
            print(Fore.CYAN + "\nAsking insurance agent about waiting periods..." + Fore.RESET)
            run2 = await insurer.run_sync(
                agent="policy_agent",
                input=f"Context: {content}. What is the waiting period for rehabilitation services?"
            )
            
            # Debug: Check response structure
            print(f"Insurance response type: {type(run2)}")
            print(f"Insurance response: {run2}")
            
            # Handle insurance response
            if hasattr(run2, 'output') and run2.output and len(run2.output) > 0:
                if hasattr(run2.output[0], 'parts') and len(run2.output[0].parts) > 0:
                    insurance_content = run2.output[0].parts[0].content
                    print(Fore.YELLOW + f"Insurance Agent: {insurance_content}" + Fore.RESET)
                else:
                    print(Fore.RED + f"Unexpected insurance response structure: {run2.output}" + Fore.RESET)
            else:
                print(Fore.RED + "No output from insurance agent" + Fore.RESET)
                
    except ConnectionError as e:
        print(Fore.RED + f"Connection error: {e}" + Fore.RESET)
        print(Fore.YELLOW + "Make sure both servers are running:" + Fore.RESET)
        print("  - Hospital server: python health_acp_server.py (port 8000)")
        print("  - Insurance server: python rag.py (port 8001)")
    except Exception as e:
        print(Fore.RED + f"Error in workflow: {e}" + Fore.RESET)


if __name__ == "__main__":
    asyncio.run(run_hospital_workflow())
    print(Fore.YELLOW + "Run completed successfully." + Fore.RESET)
    print("You can now use the agent to ask questions about the insurance policy.")
    print("Example: 'What is the waiting period for rehabilitation services?'")