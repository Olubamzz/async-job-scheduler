import asyncio
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

class AsyncScheduler:
    def __init__(self, max_retries=3):
        self.tasks = []
        self.max_retries = max_retries

    async def run_task(self, coro, task_name="Unnamed Task"):
        for attempt in range(1, self.max_retries + 1):
            try:
                logging.info(f"Starting '{task_name}' (Attempt {attempt})...")
                await coro()
                logging.info(f"✅ '{task_name}' completed successfully.")
                return
            except Exception as e:
                logging.error(f"❌ Error in '{task_name}': {e}")
                if attempt == self.max_retries:
                    logging.error(f"Exceeded retry limit for '{task_name}'.")
                else:
                    await asyncio.sleep(2 ** attempt)  # exponential backoff

    async def run_all(self):
        logging.info("🚀 Scheduler started.")
        await asyncio.gather(*[self.run_task(coro, name) for coro, name in self.tasks])
        logging.info("🏁 Scheduler finished all tasks.")

    def add_task(self, coro, name):
        self.tasks.append((coro, name))
        logging.info(f"Added task '{name}' to scheduler.")

# Example usage
async def sample_task():
    await asyncio.sleep(1)
    print(f"Task executed at {datetime.now()}")

if __name__ == "__main__":
    scheduler = AsyncScheduler()
    scheduler.add_task(sample_task, "Data Sync Job")
    asyncio.run(scheduler.run_all())

Added base async job scheduler with retry and logging system
