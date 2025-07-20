# tests/test_agents.py
import pytest
import asyncio
from unittest.mock import Mock, patch

class TestAgentSuite:
    def test_documentation_agent(self):
        """Test documentation generation"""
        agent = DocumentationAgent()
        sample_code = """
        def calculate_sum(a: int, b: int) -> int:
            return a + b
        """
        
        # Mock the API response
        with patch.object(agent.agent, 'run') as mock_run:
            mock_run.return_value.text = "## calculate_sum\n\nAdds two integers."
            
            result = asyncio.run(agent.process_file("test.py", sample_code))
            
            assert result['status'] == 'success'
            assert 'calculate_sum' in result['documentation']
    
    def test_rate_limiter(self):
        """Test rate limiting functionality"""
        limiter = GoogleAIRateLimiter()
        
        # Should not block first few requests
        for i in range(5):
            asyncio.run(limiter.wait_if_needed())
        
        assert limiter.daily_count == 5
        assert len(limiter.request_times) == 5
