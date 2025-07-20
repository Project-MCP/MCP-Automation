# agents/doc_agent/doc_generator.py - CORRECTED MODEL NAME

import os
import sys
import logging
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

# Ensure the project root is on the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load environment variables from .env file at the project root
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentationAgent:
    """
    An AI agent that specializes in generating technical documentation for source code.
    """
    def __init__(self):
        logger.info("Initializing DocumentationAgent...")
        try:
            # Configure the Google AI API
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            genai.configure(api_key=api_key)
            # CHANGED: Use the correct model name
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Define the instruction as a system message
            self.system_instruction = """
            You are an expert technical writer for a software development team. Your task is to generate clear,
            concise, and accurate documentation for the provided source code.

            Follow these rules:
            1. Analyze the code's purpose, functions, classes, and logic.
            2. Generate documentation in Markdown format.
            3. For each function or method, describe its purpose, parameters (including their types), and what it returns.
            4. Provide a clear usage example for each public function.
            5. Adhere to the standard documentation style for the given programming language.
            """
            
            logger.info("✅ DocumentationAgent initialized successfully.")
        except Exception as e:
            logger.error(f"❌ Failed to initialize DocumentationAgent: {e}")
            raise

    async def generate_documentation(self, file_path: str, code_content: str) -> str:
        """
        Takes a code snippet and returns AI-generated documentation in Markdown.
        """
        prompt = f"""
        {self.system_instruction}

        Please generate technical documentation for the following code.

        File Path: `{file_path}`

        Source Code:
        ```
        {code_content}
        ```
        """
        logger.info(f"Generating documentation for {file_path}...")
        try:
            # Use the direct Google Generative AI client
            response = await self.model.generate_content_async(prompt)
            
            logger.info(f"✅ Successfully generated documentation for {file_path}.")
            return response.text
            
        except Exception as e:
            logger.error(f"❌ Error during documentation generation: {e}")
            return f"Error: Could not generate documentation. Details: {e}"

# To allow direct testing of this file
if __name__ == '__main__':
    async def test_agent():
        print("Running a direct test of the DocumentationAgent...")
        agent = DocumentationAgent()
        sample_code = "def add(a, b):\n    return a + b"
        documentation = await agent.generate_documentation("src/test.py", sample_code)
        print("\n--- Generated Documentation ---")
        print(documentation)
        print("\n--- Test Complete ---")

    asyncio.run(test_agent())
