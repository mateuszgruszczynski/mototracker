import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from app.scraper.events import cleanup, scan_queues, scan_snapshots

router = APIRouter(prefix="/scans")


@router.get("/{scan_id}/stream")
async def stream(scan_id: int):
    if scan_id not in scan_queues and scan_id not in scan_snapshots:
        return JSONResponse({"detail": "Scan not found"}, status_code=404)

    async def generator():
        # Send snapshot immediately for late subscribers.
        snapshot = scan_snapshots.get(scan_id)
        if snapshot:
            yield {"data": json.dumps(snapshot)}
            if snapshot.get("type") in ("done", "failed"):
                cleanup(scan_id)
                return

        queue = scan_queues.get(scan_id)
        if queue is None:
            return

        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30)
            except asyncio.TimeoutError:
                yield {"comment": "keepalive"}
                continue
            yield {"data": json.dumps(event)}
            if event.get("type") in ("done", "failed"):
                cleanup(scan_id)
                break

    return EventSourceResponse(generator())
