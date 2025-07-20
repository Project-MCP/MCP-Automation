# agents/review_agent/code_reviewer.py
class CodeReviewAgent:
    def __init__(self):
        self.agent = LlmAgent(
            name="code_reviewer",
            model="gemini-1.5-flash-001", 
            description="Performs automated code reviews",
            instruction="""
            Review code changes for:
            1. Code quality and style issues
            2. Potential bugs and logic errors
            3. Security vulnerabilities
            4. Performance concerns
            5. Best practice violations
            
            Provide constructive feedback with specific line references.
            """,
            temperature=0.2
        )
    
    async def review_pull_request(self, diff: str, files_changed: list):
        """Review a pull request diff"""
        prompt = f"""
        Review this pull request:
        
        Files changed: {', '.join(files_changed)}
        
        Diff:
        {diff}
        
        Provide review feedback in this format:
        ## Code Quality Issues
        ## Security Concerns  
        ## Performance Notes
        ## Best Practices
        ## Overall Assessment
        """
        
        response = await self.agent.run(prompt)
        return {
            'review': response.text,
            'files_reviewed': files_changed,
            'timestamp': datetime.now().isoformat()
        }
