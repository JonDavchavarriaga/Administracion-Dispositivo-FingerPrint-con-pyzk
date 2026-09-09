import asyncio
from datetime import datetime, timezone
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect


class DeviceStatusManager:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._loop: asyncio.AbstractEventLoop | None = None

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)
        self._loop = asyncio.get_running_loop()

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    async def broadcast(self, event: dict[str, Any]) -> None:
        stale_connections = []
        for websocket in tuple(self._connections):
            try:
                await websocket.send_json(event)
            except (WebSocketDisconnect, RuntimeError):
                stale_connections.append(websocket)
        for websocket in stale_connections:
            self.disconnect(websocket)

    def publish(self, event: dict[str, Any]) -> None:
        if self._loop is None or not self._loop.is_running():
            return
        asyncio.run_coroutine_threadsafe(self.broadcast(event), self._loop)


device_status_manager = DeviceStatusManager()


def publish_device_status(
    device_id: int,
    status: str,
    *,
    job_id: str | None = None,
    error: str | None = None,
) -> None:
    device_status_manager.publish(
        {
            "type": "device_status_changed",
            "device_id": device_id,
            "status": status,
            "job_id": job_id,
            "error": error,
            "occurred_at": datetime.now(timezone.utc).isoformat(),
        }
    )
