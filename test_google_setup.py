# test_google_setup.py
import sys
import os
import subprocess
from dotenv import load_dotenv

def test_python():
    print(f"✅ Python version: {sys.version}")
    return True

def test_docker():
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        print(f"✅ Docker: {result.stdout.strip()}")
        return True
    except:
        print("❌ Docker not working")
        return False

def test_google_ai_studio():
    try:
        load_dotenv()
        import google.generativeai as genai
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Google API key not found in .env file")
            return False
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content("Say hello!")
        
        print(f"✅ Google AI Studio working: {response.text[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Google AI Studio error: {e}")
        return False

def test_adk():
    try:
        from google.adk.agents import LlmAgent
        print("✅ Google ADK installed and working")
        return True
    except Exception as e:
        print(f"❌ ADK error: {e}")
        return False

def test_environment():
    try:
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key and len(api_key) > 30:
            print("✅ Environment variables configured")
            return True
        else:
            print("❌ Google API key not properly configured")
            return False
    except:
        print("❌ Environment configuration error")
        return False

if __name__ == "__main__":
    print("🧪 Testing Google AI Studio + ADK Development Environment...\n")
    
    tests = [
        test_python, 
        test_docker, 
        test_environment,
        test_google_ai_studio, 
        test_adk
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print(f"📊 Results: {sum(results)}/{len(results)} tests passed")
    
    if all(results):
        print("🎉 Google AI Studio + ADK environment setup complete!")
        print("💡 You're ready to build powerful AI automation agents!")
    else:
        print("⚠️  Some components need fixing before proceeding.")
