import asyncio
from collections import deque

class JobQueue:
    def __init__(self):
        self.queue = deque()
        self.running = False

    def add_job(self, coro, name):
        self.queue.append((coro, name))
        print(f"📦 Job '{name}' added to queue.")

    async def run(self):
        self.running = True
        while self.queue:
            coro, name = self.queue.popleft()
            print(f"🚀 Executing job '{name}'...")
            try:
                await coro()
                print(f"✅ Job '{name}' completed.")
            except Exception as e:
                print(f"❌ Job '{name}' failed: {e}")
        self.running = False

Added JobQueue class to manage async job execution with FIFO logic
