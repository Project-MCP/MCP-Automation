# agents/release_agent/release_generator.py
class ReleaseNotesAgent:
    def __init__(self):
        self.agent = LlmAgent(
            name="release_notes_generator", 
            model="gemini-1.5-flash-001",
            description="Generates user-friendly release notes from commits",
            instruction="""
            Transform git commits into engaging release notes:
            1. Group commits by feature/bugfix/improvement
            2. Write user-friendly descriptions
            3. Highlight breaking changes
            4. Add emoji for visual appeal
            5. Include migration guides if needed
            """,
            temperature=0.4
        )
    
    async def generate_from_commits(self, commits: list, version: str):
        """Generate release notes from commit history"""
        commit_summary = "\n".join([
            f"- {commit['message']} ({commit['author']})"
            for commit in commits
        ])
        
        prompt = f"""
        Create release notes for version {version}:
        
        Commits:
        {commit_summary}
        
        Format as professional release notes with sections for:
        - New Features 🚀
        - Bug Fixes 🐛  
        - Improvements ⚡
        - Breaking Changes ⚠️
        """
        
        response = await self.agent.run(prompt)
        return response.text
