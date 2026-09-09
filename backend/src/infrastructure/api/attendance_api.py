import os

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from typing import List, Optional
from src.application.services.attendance_service import AttendanceService
from src.application.services.device_config_service import DeviceConfigService
from src.application.services.device_sync_service import DeviceSyncService
from src.application.services.user_service import UserService
from src.application.services.cost_center_service import CostCenterService
from src.infrastructure.queue.celery_app import synchronize_device
from src.infrastructure.realtime.device_status_manager import (
    device_status_manager,
)

class DeviceRegisterRequest(BaseModel):
    name: str
    ip: str
    port: int = 4370
    interval_seconds: int = 60

class DeviceUpdateRequest(BaseModel):
    name: str
    ip: str
    port: int
    interval_seconds: int

class UserUpdateRequest(BaseModel):
    name: str
    is_active: bool

class AssignCostCenterRequest(BaseModel):
    cost_center_id: Optional[int]

class CostCenterRequest(BaseModel):
    name: str


def create_app(
    device_repo,
    attendance_repo,
    sync_service,
    user_repo,
    cost_center_repo
):
    app = FastAPI(title="Sistema de Asistencia")
    openapi_tags=[
        {"name": "Users", "description": "User management"},
        {"name": "Cost Centers", "description": "Cost center management"},
        {"name": "Devices", "description": "Biometric device management"},
        {"name": "Sync", "description": "Device synchronization"},
        {"name": "Attendance", "description": "Attendance records"},
    ]
    device_service = DeviceConfigService(
        repository=device_repo,
        sync_service=sync_service
    )
    attendance_service = AttendanceService(attendance_repo)
    user_service = UserService(user_repo)
    cost_center_service = CostCenterService(cost_center_repo)

    @app.websocket("/ws/devices")
    async def device_status_websocket(websocket: WebSocket):
        await device_status_manager.connect(websocket)
        try:
            devices = device_repo.find_all()
            await websocket.send_json(
                {
                    "type": "device_snapshot",
                    "devices": [
                        {
                            "device_id": device.device_id,
                            "name": device.name,
                            "status": "unknown" if device.is_active else "disabled",
                            "last_sync_at": (
                                device.last_sync_at.isoformat()
                                if device.last_sync_at
                                else None
                            ),
                        }
                        for device in devices
                    ],
                }
            )
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            device_status_manager.disconnect(websocket)

    @app.get("/users", tags=["Users"])
    def list_users():
        return [u.__dict__ for u in user_service.list_users()]

    @app.put("/users/{user_id}", tags=["Users"])
    def update_user(user_id: int, request: UserUpdateRequest):
        try:
            user = user_service.update_user(
                user_id=user_id,
                name=request.name,
                is_active=request.is_active
            )
            return user.__dict__
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.patch("/users/{user_id}/cost-center", tags=["Users"])
    def assign_cost_center(user_id: int, request: AssignCostCenterRequest):
        try:
            user = user_service.assign_cost_center(
                user_id=user_id,
                cost_center_id=request.cost_center_id
            )
            return user.__dict__
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    #======== Cost Centers ========
    @app.post("/cost-centers", tags=["Cost Centers"])
    def create_cost_center(request: CostCenterRequest):
        cc = cost_center_service.register_cost_center(request.name)
        return cc.__dict__

    @app.get("/cost-centers", tags=["Cost Centers"])
    def list_cost_centers():
        return [c.__dict__ for c in cost_center_service.list_cost_centers()]

    @app.put("/cost-centers/{cost_center_id}", tags=["Cost Centers"])
    def update_cost_center(cost_center_id: int, request: CostCenterRequest):
        cc = cost_center_service.repository.find_by_id(cost_center_id)
        if not cc:
            raise HTTPException(status_code=404, detail="Cost center not found")

        cc.name = request.name
        cc = cost_center_service.repository.update(cc)
        return cc.__dict__

    @app.delete("/cost-centers/{cost_center_id}", tags=["Cost Centers"])
    def delete_cost_center(cost_center_id: int):
        cost_center_service.repository.delete(cost_center_id)
        return {"status": "deleted"}

    #======== Devices ========
    @app.post("/devices", tags=["Devices"])
    def register_device(request: DeviceRegisterRequest):
        device = device_service.create_device(
            name=request.name,
            ip=request.ip,
            port=request.port,
            interval_seconds=request.interval_seconds
        )
        return device.__dict__

    @app.get("/devices", tags=["Devices"])
    def list_devices():
        return [d.__dict__ for d in device_service.list_devices()]

    @app.put("/devices/{device_id}", tags=["Devices"])
    def update_device(device_id: int, request: DeviceUpdateRequest):
        device = device_service.update_device(
            device_id=device_id,
            name=request.name,
            ip=request.ip,
            port=request.port,
            interval_seconds=request.interval_seconds
        )
        return device.__dict__

    @app.patch("/devices/{device_id}/activate", tags=["Devices"])
    def activate_device(device_id: int):
        device_service.activate_device(device_id, True)
        return {"status": "activated"}

    @app.patch("/devices/{device_id}/deactivate", tags=["Devices"])
    def deactivate_device(device_id: int):
        try:
            device_service.activate_device(device_id, False)
            return {"status": "deactivated"}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    #======== Sync ========
    @app.post("/devices/{device_id}/sync", tags=["Sync"])
    def manual_sync(device_id: int):
        device = device_repo.find_by_id(device_id)
        if not device or not device.is_active:
            raise HTTPException(status_code=404, detail="Device not found or inactive")
        if os.getenv("MOCK_MODE", "False").lower() == "true":
            result = sync_service.sync_device(device_id)
            return {"status": "completed", "device_id": device_id, "result": result}
        task = synchronize_device.delay(device_id)
        return {"status": "queued", "task_id": task.id, "device_id": device_id}

    @app.post("/devices/sync-all", tags=["Sync"])
    def sync_all():
        devices = device_repo.find_active()
        if os.getenv("MOCK_MODE", "False").lower() == "true":
            results = [sync_service.sync_device(d.device_id) for d in devices]
            return {"status": "completed", "results": results}
        task_ids = [synchronize_device.delay(d.device_id).id for d in devices]
        return {"status": "queued", "task_ids": task_ids}

    #======== Attendance Records ========

    @app.get("/attendance" , tags=["Attendance"])
    def get_attendance():
        return [r.__dict__ for r in attendance_repo.find_all()]


    return app
