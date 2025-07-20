# scripts/agent_selector.py
import os
import json
from datetime import datetime, timedelta

class AgentSelector:
    def __init__(self):
        self.github_event = os.getenv('GITHUB_EVENT_NAME')
        self.changed_files = self._get_changed_files()
    
    def select_agents(self):
        """Determine which agents should run based on context"""
        agents_to_run = []
        
        if self.github_event == 'push':
            if self._has_code_changes():
                agents_to_run.extend(['documentation', 'risk-analysis'])
            
        elif self.github_event == 'pull_request':
            agents_to_run.extend(['code-review', 'risk-analysis'])
            
        elif self.github_event == 'schedule':
            agents_to_run.extend(['velocity-prediction', 'capacity-forecast'])
        
        # Always run dependency updates weekly
        if datetime.now().weekday() == 0:  # Monday
            agents_to_run.append('dependency-update')
        
        print(f"::set-output name=agents::{json.dumps(agents_to_run)}")
        return agents_to_run
