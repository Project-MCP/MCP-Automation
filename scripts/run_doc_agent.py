# scripts/run_doc_agent.py

import asyncio
import os
import sys

# Add project root to Python path to find the agent module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.doc_agent.doc_generator import DocumentationAgent

async def main():
    """
    A script to manually trigger the documentation agent for testing purposes.
    """
    print("--- Manual Documentation Agent Trigger ---")

    # The file we want to document
    file_to_document = "src/utils.py"

    if not os.path.exists(file_to_document):
        print(f"❌ Error: The file '{file_to_document}' does not exist. Please create it first.")
        return

    # Read the content of the sample code file
    with open(file_to_document, 'r') as f:
        code_content = f.read()

    print(f"📄 Read {len(code_content)} characters from '{file_to_document}'.")

    # Initialize our agent
    doc_agent = DocumentationAgent()

    # Generate the documentation
    generated_docs = await doc_agent.generate_documentation(
        file_path=file_to_document,
        code_content=code_content
    )

    # Print the final result
    print("\n" + "="*50)
    print("🤖 AI-Generated Documentation:")
    print("="*50)
    print(generated_docs)
    print("="*50)
    print("\n--- Task Complete ---")

if __name__ == "__main__":
    asyncio.run(main())

