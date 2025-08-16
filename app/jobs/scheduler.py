from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from app.jobs.nightly_update import update_data

scheduler = AsyncIOScheduler()

def start_scheduler():
    """Start the background job scheduler"""
    # Run every day at 8 AM UTC
    scheduler.add_job(
        update_data,
        CronTrigger(hour=8, minute=0),
        id='nightly_update',
        name='Update draft picks nightly'
    )
    scheduler.start()
    logging.info("Scheduler started - nightly updates will run at 8 AM UTC")

def stop_scheduler():
    """Stop the background job scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logging.info("Scheduler stopped")
