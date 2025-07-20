from google.adk.agents import LlmAgent
import asyncio
import sys

async def main():
    try:
        agent = LlmAgent(
            name="test",
            model="gemini-1.0-pro",
            description="Test agent",
            instruction="You are a helpful AI assistant."
        )
        print("Agent created successfully")
        print("\nAvailable methods:")
        for method in dir(agent):
            if not method.startswith('_'):
                print(f"- {method}")
        
        print("\nTrying to use agent...")
        response = await agent.run("Say hello!")
        print(f"Response: {response.text if hasattr(response, 'text') else response}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    asyncio.run(main())
