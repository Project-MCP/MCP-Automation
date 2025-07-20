# agents/risk_agent/risk_analyzer.py
class DeploymentRiskAnalyzer:
    def __init__(self):
        self.agent = LlmAgent(
            name="risk_analyzer",
            model="gemini-1.5-flash-001",
            description="Analyzes deployment risks",
            instruction="""
            Assess deployment risk based on:
            1. Code changes complexity
            2. Number of files modified
            3. Test coverage changes
            4. Dependencies updates
            5. Historical failure patterns
            
            Rate risk as: LOW, MEDIUM, HIGH with explanations.
            """,
            temperature=0.2
        )
    
    def calculate_risk_score(self, deployment_data: dict):
        """Calculate basic risk score"""
        score = 0
        
        # File change impact
        if deployment_data['files_changed'] > 50:
            score += 3
        elif deployment_data['files_changed'] > 20:
            score += 2
        elif deployment_data['files_changed'] > 5:
            score += 1
            
        # Test coverage
        if deployment_data.get('test_coverage_drop', 0) > 5:
            score += 2
            
        # Dependency updates
        if deployment_data.get('dependency_updates', 0) > 10:
            score += 2
        
        return {
            'score': score,
            'level': 'LOW' if score <= 2 else 'MEDIUM' if score <= 5 else 'HIGH',
            'recommendations': self._get_recommendations(score)
        }
