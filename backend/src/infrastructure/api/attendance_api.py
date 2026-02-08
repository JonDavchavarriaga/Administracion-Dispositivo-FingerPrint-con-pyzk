from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import List, Optional
from src.application.sevices.attendance_service import AttendanceService
from src.application.sevices.device_config_service import DeviceConfigService
from src.application.sevices.device_sync_service import DeviceSyncService
from src.application.sevices.user_service import UserService
from src.application.sevices.cost_center_service import CostCenterService

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
        {"name": "Users", "description": "Gestión de usuarios"},
        {"name": "Cost Centers", "description": "Centros de costo"},
        {"name": "Devices", "description": "Dispositivos biométricos"},
        {"name": "Sync", "description": "Sincronización de dispositivos"},
        {"name": "Attendance", "description": "Marcaciones y asistencias"},
    ]
    device_service = DeviceConfigService(
        repository=device_repo,
        sync_service=sync_service
    )
    attendance_service = AttendanceService(attendance_repo)
    user_service = UserService(user_repo)
    cost_center_service = CostCenterService(cost_center_repo)

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
        sync_service.sync_device(device_id)
        return {"status": "sync executed"}

    @app.post("/devices/sync-all", tags=["Sync"])
    def sync_all():
        devices = device_repo.find_active()
        for d in devices:
            sync_service.sync_device(d.device_id)
        return {"status": "sync all executed"}

    #======== Attendance Records ========

    @app.get("/attendance" , tags=["Attendance"])
    def get_attendance():
        return [r.__dict__ for r in attendance_repo.find_all()]


    return app




