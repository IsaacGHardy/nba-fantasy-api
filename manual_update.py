import asyncio
import logging
from app.jobs.nightly_update import update_data

# Set up logging to see what happens
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
    
async def main():
    logging.info("Starting nightly update test...")
    try:
        await update_data()
        logging.info("✅ Nightly update completed successfully!")
    except Exception as e:
        logging.error(f"Nightly update failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())