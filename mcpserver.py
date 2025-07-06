from colorama import Fore
from mcp.server.fastmcp import FastMCP
import json
import requests

mcp = FastMCP("doctorserver")

@mcp.tool()
def list_doctors(state: str) -> str:
    """This tool returns doctors theat may be near you.
    
    Args:
        state: the two letter state code that you live in.
        Example payload: "CA"

    Returns:
        str: A list of doctors that may be near you.
        Example Response: "{"DOC001":{"name":"Dr. Smith","specialty":"Cardiology","location":"Los Angeles, CA"},"DOC002":{"name":"Dr. Jones","specialty":"Cardiology"...}...}"
    """
    url = 'https://raw.githubusercontent.com/nicknochnack/ACPWalkthrough/refs/heads/main/doctors.json'
    response = requests.get(url)
    doctors = json.loads(response.text)

    matches = [doctor for doctor in doctors.values() if doctor['address']['state'] == state]
    return str(matches)

if __name__ == "__main__":
    mcp.run(transport="stdio")
    print(Fore.YELLOW + "Doctor server is running. You can now use the list_doctors tool." + Fore.RESET)
    print(Fore.YELLOW + "Example usage: list_doctors('CA')" + Fore.RESET)
    print(Fore.YELLOW + "This will return a list of doctors in California." + Fore.RESET)