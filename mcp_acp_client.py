import asyncio 
import nest_asyncio
from acp_sdk.client import Client
from colorama import Fore

nest_asyncio.apply()

async def run_doctor_workflow() -> None:
    async with Client(base_url="http://localhost:8000") as hospital:
        run1 = await hospital.run_sync(
            agent="doctor_agent",
            input="I'm based in Atlanta, GA. Are there any Cardiologists near me?"
        )
        # guard against empty output
        if not run1.output:
            print(Fore.RED + "doctor_agent returned no output" + Fore.RESET)
            return

        msg = run1.output[0]
        if not msg.parts:
            print(Fore.RED + "doctor_agent message has no parts" + Fore.RESET)
            return

        content = msg.parts[0].content
        print(Fore.YELLOW + content + Fore.RESET)


if __name__ == "__main__":
    asyncio.run(run_doctor_workflow())