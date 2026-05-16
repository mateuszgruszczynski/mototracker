import asyncio

scan_queues: dict[int, asyncio.Queue] = {}
scan_snapshots: dict[int, dict] = {}


def emit(scan_id: int, event: dict) -> None:
    if scan_id not in scan_queues:
        scan_queues[scan_id] = asyncio.Queue()
    scan_snapshots[scan_id] = event
    scan_queues[scan_id].put_nowait(event)


def cleanup(scan_id: int) -> None:
    scan_queues.pop(scan_id, None)
    scan_snapshots.pop(scan_id, None)
