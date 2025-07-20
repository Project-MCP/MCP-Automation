# agents/test_agent/simple_agent.py
import os
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

# Load environment variables from the .env file in the project root
from dotenv import load_dotenv
load_dotenv()

# Create a simple documentation agent
doc_agent = LlmAgent(
    name="documentation_generator",
    model="gemini-1.5-flash-001",  # Use the free tier model
    description="An AI agent that generates technical documentation for code",
    instruction="""
    You are a technical documentation expert. When given code, you will:
    1. Analyze the code structure and functionality.
    2. Generate comprehensive documentation in Markdown format.
    3. Include function descriptions, parameters, return values, and examples.
    4. Follow standard documentation practices.
    """,
    tools=[google_search]  # Optional: add search capability to the agent
)

if __name__ == "__main__":
    # This block runs only when you execute this script directly
    # It's a great way to test that the agent was created without errors
    print("✅ Documentation Agent created successfully!")
    print(f"   Agent name: {doc_agent.name}")
    print(f"   Model being used: {doc_agent.model}")
