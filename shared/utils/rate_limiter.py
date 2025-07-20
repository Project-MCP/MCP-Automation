# shared/utils/rate_limiter.py
import asyncio
from datetime import datetime, timedelta

class GoogleAIRateLimiter:
    def __init__(self):
        self.requests_per_minute = 10  # Free tier limit
        self.daily_limit = 200
        self.request_times = []
        self.daily_count = 0
        self.reset_date = datetime.now().date()
    
    async def wait_if_needed(self):
        """Implement rate limiting logic"""
        now = datetime.now()
        
        # Reset daily counter
        if now.date() != self.reset_date:
            self.daily_count = 0
            self.reset_date = now.date()
        
        # Check daily limit
        if self.daily_count >= self.daily_limit:
            raise Exception("Daily API limit reached")
        
        # Remove old requests (older than 1 minute)
        minute_ago = now - timedelta(minutes=1)
        self.request_times = [t for t in self.request_times if t > minute_ago]
        
        # Check minute limit
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = 60 - (now - min(self.request_times)).seconds
            await asyncio.sleep(sleep_time)
        
        self.request_times.append(now)
        self.daily_count += 1
