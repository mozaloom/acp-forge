from crewai_tools import RagTool
import os
from dotenv import load_dotenv
load_dotenv()

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

# Test the RAG tool directly
rag_tool = RagTool(
    config=config,
    chunk_size=1200,
    chunk_overlap=200
)

print("Testing RAG tool directly...")
try:
    # Test search directly
    result = rag_tool._run("waiting period rehabilitation")
    print("RAG tool result:", result)
except Exception as e:
    print("Error testing RAG tool:", e)
