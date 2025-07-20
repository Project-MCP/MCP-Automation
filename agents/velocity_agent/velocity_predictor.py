# agents/velocity_agent/velocity_predictor.py
class VelocityPredictor:
    def __init__(self):
        self.agent = LlmAgent(
            name="velocity_predictor",
            model="gemini-1.5-flash-001",
            description="Predicts sprint velocity based on historical data",
            instruction="""
            Analyze sprint data and predict velocity:
            1. Review historical sprint completion rates
            2. Consider team capacity changes
            3. Account for complexity trends
            4. Provide confidence intervals
            5. Suggest capacity adjustments
            """,
            temperature=0.1  # Low temperature for consistent predictions
        )
    
    def analyze_historical_data(self, sprint_history: list):
        """Analyze past sprint performance"""
        return {
            'average_velocity': sum(s['completed_points'] for s in sprint_history) / len(sprint_history),
            'velocity_trend': self._calculate_trend(sprint_history),
            'consistency_score': self._calculate_consistency(sprint_history)
        }
