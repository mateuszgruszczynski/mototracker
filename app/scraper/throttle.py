import asyncio
import random
import time


class AsyncThrottler:
    def __init__(self, min_seconds: float, jitter_seconds: float):
        self._min = min_seconds
        self._jitter = jitter_seconds
        self._last_request_at: float = 0.0

    async def wait(self) -> None:
        delay = self._min + random.uniform(0, self._jitter)
        elapsed = time.monotonic() - self._last_request_at
        remaining = delay - elapsed
        if remaining > 0:
            await asyncio.sleep(remaining)
        self._last_request_at = time.monotonic()
