import sys
import os
import json
import logging
import traceback
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Load environment variables
env_path = os.path.join(project_root, '.env')
load_dotenv(env_path)

def check_environment():
    """Check all required environment variables and credentials"""
    logger.info("Checking environment setup...")
    
    # Check environment variables
    required_vars = ['GOOGLE_API_KEY', 'GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_CLOUD_PROJECT']
    all_set = True
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            logger.error(f"❌ Missing environment variable: {var}")
            all_set = False
        else:
            logger.info(f"✅ {var} is set")
            
            # Check credentials file if it's the GOOGLE_APPLICATION_CREDENTIALS
            if var == 'GOOGLE_APPLICATION_CREDENTIALS':
                creds_path = os.path.join(project_root, value)
                if os.path.exists(creds_path):
                    logger.info(f"✅ Credentials file exists at {creds_path}")
                    # Check file permissions
                    try:
                        with open(creds_path, 'r') as f:
                            creds = json.load(f)
                            logger.info(f"✅ Credentials file is valid JSON")
                            logger.info(f"✅ Project ID in credentials: {creds.get('project_id')}")
                    except Exception as e:
                        logger.error(f"❌ Error reading credentials file: {e}")
                        all_set = False
                else:
                    logger.error(f"❌ Credentials file not found at {creds_path}")
                    all_set = False
    
    return all_set

async def test_llm_agent():
    """Test LlmAgent with multiple models"""
    from google.adk.agents import LlmAgent
    logger.info("Successfully imported LlmAgent")
    
    # Models to try
    models = [
        "gemini-1.0-pro",
        "gemini-1.5-pro-001",
        "gemini-1.5-flash-001"
    ]
    
    for model in models:
        logger.info(f"\nTesting model: {model}")
        try:
            # Initialize agent
            agent = LlmAgent(
                name="test_agent",
                model=model,
                description="Test agent",
                instruction="You are a test agent."
            )
            logger.info(f"✅ Initialized agent with {model}")
            
            # Log available methods
            methods = [m for m in dir(agent) if not m.startswith('_')]
            logger.info(f"Available methods: {methods}")
            
            # Try methods
            try:
                logger.info("Testing run() method...")
                response = await agent.run("Say hello")
                logger.info(f"✅ run() successful: {response.text if hasattr(response, 'text') else response}")
                return  # Success
            except AttributeError:
                logger.info("run() not available, trying complete()...")
            
            try:
                logger.info("Testing complete() method...")
                response = await agent.complete(prompt="Say hello", temperature=0.3)
                logger.info(f"✅ complete() successful: {response.text if hasattr(response, 'text') else response}")
                return  # Success
            except AttributeError:
                logger.error("Neither run() nor complete() methods are available")
            
        except Exception as e:
            logger.error(f"Error with {model}: {str(e)}")
            continue
    
    raise Exception("All models failed")

if __name__ == "__main__":
    try:
        # First check environment
        if not check_environment():
            raise Exception("Environment check failed")
        
        # Then run the agent test
        import asyncio
        asyncio.run(test_llm_agent())
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
