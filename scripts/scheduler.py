#!/usr/bin/env python3
"""
Agent Scheduler Service - FINAL CORRECTED VERSION
"""
import os
import sys
import time
import asyncio
import logging
import schedule
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
sys.path.append('/app')

class AgentScheduler:
    def __init__(self):
        self.running = True
        logger.info("🕐 Agent Scheduler initialized")

    async def health_check_async(self):
        logger.info(f"✅ Scheduler health check running at {datetime.now()}")

    def schedule_jobs(self):
        logger.info("📅 Scheduling jobs...")
        schedule.every().hour.do(lambda: asyncio.run(self.health_check_async()))
        logger.info("   - Hourly health checks scheduled.")
        logger.info("✅ Jobs scheduled successfully.")

    def run(self):
        self.schedule_jobs()
        logger.info("🚀 Agent Scheduler started successfully")
        asyncio.run(self.health_check_async())

        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.running = False
        finally:
            logger.info("🔚 Agent Scheduler shutting down")

def main():
    logger.info("🎯 Starting Agent Scheduler Service")
    scheduler = AgentScheduler()
    scheduler.run()

if __name__ == "__main__":
    main()
