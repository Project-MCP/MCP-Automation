#!/usr/bin/env python3
"""
Test script for the AI agents API
"""
import asyncio
import aiohttp
import json
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

async def test_documentation_api():
    """Test the documentation generation API endpoint."""
    
    # Read our sample code file
    with open('src/utils.py', 'r') as f:
        code_content = f.read()
    
    # Prepare the API request
    url = "http://localhost:8000/agents/documentation/generate"
    payload = {
        "file_path": "src/utils.py",
        "code_content": code_content
    }
    
    print("🧪 Testing Documentation API...")
    print(f"📡 Making request to: {url}")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ API Request Successful!")
                    print(f"📄 File: {result['file_path']}")
                    print(f"⏱️  Processing time: {result['processing_time']:.2f} seconds")
                    print(f"✨ Status: {result['status']}")
                    print("\n" + "="*60)
                    print("📝 Generated Documentation:")
                    print("="*60)
                    print(result['documentation'])
                    print("="*60)
                else:
                    print(f"❌ API Request Failed: {response.status}")
                    print(await response.text())
                    
        except aiohttp.ClientConnectorError:
            print("❌ Could not connect to API. Make sure the service is running on localhost:8000")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_documentation_api())
