import sys
import os
import traceback
import logging
import json
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

# Check environment setup
logger.info("Checking environment setup...")
required_vars = ['GOOGLE_API_KEY', 'GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_CLOUD_PROJECT']
env_status = {}
for var in required_vars:
    env_status[var] = {
        'present': var in os.environ,
        'value': '[SET]' if var in os.environ and os.environ[var] else '[EMPTY]'
    }
    logger.info(f"{var}: {json.dumps(env_status[var])}")

# Check credentials file
creds_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
if creds_path:
    full_path = os.path.join(project_root, creds_path)
    logger.info(f"Checking credentials file: {full_path}")
    if os.path.exists(full_path):
        logger.info("✅ Credentials file exists")
    else:
        logger.error(f"❌ Credentials file not found at {full_path}")

try:
    logger.info("Attempting to import LlmAgent...")
    from google.adk.agents import LlmAgent
    logger.info("✅ Successfully imported LlmAgent")
    
    async def test_llm_agent():
        """Test LlmAgent initialization and basic functionality"""
        # Set up logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        # Models to test
        models_to_try = [
            "gemini-1.0-pro",
            "gemini-1.0-pro-001",
            "gemini-1.5-pro-001",
            "gemini-1.5-flash-001"
        ]
        
        success = False
        errors = []
        
        # Try each model until one works
        for model_name in models_to_try:
            if success:
                break
                
            logger.info(f"Testing with model: {model_name}")
            print(f"\n=== Testing with model: {model_name} ===")
            
            try:
                # Initialize agent
                agent = LlmAgent(
                    name="test_agent",
                    model=model_name,
                    description="A test agent for verifying LlmAgent functionality",
                    instruction="""You are a test agent. 
                    Keep responses very short and simple.
                    Start every response with 'Test response:'"""
                )
                logger.info("Agent initialized successfully")
                print(f"✅ Agent initialized with {model_name}")
                
                # List available methods
                methods = [m for m in dir(agent) if not m.startswith('_')]
                logger.debug(f"Available methods: {methods}")
                print("\nAvailable methods:")
                for method in methods:
                    print(f"- {method}")
                
                # Try to use the agent
                logger.info("Attempting to use agent...")
                try:
                    response = await agent.run("Say hello")
                    print(f"✅ Success! Response: {response.text if hasattr(response, 'text') else response}")
                    success = True
                    break
                except AttributeError:
                    logger.info("run() failed, trying complete()...")
                    response = await agent.complete(prompt="Say hello", temperature=0.3)
                    print(f"✅ Success! Response: {response.text if hasattr(response, 'text') else response}")
                    success = True
                    break
                    
            except Exception as e:
                error_msg = f"Failed with model {model_name}: {str(e)}"
                logger.error(error_msg)
                print(f"❌ {error_msg}")
                errors.append(error_msg)
                continue
        
        if not success:
            raise Exception(f"All models failed: {'; '.join(errors)}")
            
            try:
                print("\nTesting agent.complete()...")  # Using complete() as seen in doc_generator.py
                response = await agent.complete(
                    prompt="Say hello",
                    temperature=0.3
                )
                print(f"✅ Response received: {response.text if hasattr(response, 'text') else response}")
            except AttributeError:
                print("\nTrying agent.run() instead...")
                response = await agent.run("Say hello")
                print(f"✅ Response received: {response.text if hasattr(response, 'text') else response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                print("\nAvailable methods on agent:")
                for attr in dir(agent):
                    if not attr.startswith('_'):
                        print(f"- {attr}: {type(getattr(agent, attr))}")
                raise
            
        except Exception as e:
            print(f"Error: {str(e)}")
            raise

    # Run the async test
    import asyncio
    asyncio.run(test_llm_agent())

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
