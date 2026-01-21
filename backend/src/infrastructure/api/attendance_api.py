from fastapi import FastAPI
from pydantic import BaseModel

from src.application.attendance_service import AttendanceService
from src.application.device_config_service import DeviceConfigService


class DeviceRegisterRequest(BaseModel):
    name: str
    ip: str
    port: int = 4370
    interval_seconds: int = 300


def create_app(device_repo, attendance_repo, sync_service):
    app = FastAPI(title="Sistema de Asistencia")

    device_service = DeviceConfigService(device_repo)
    attendance_service = AttendanceService(attendance_repo)

    @app.post("/devices")
    def register_device(request: DeviceRegisterRequest):
        print("POST /devices ejecutado")
        device = device_service.register_device(
            name=request.name,
            ip=request.ip,
            port=request.port,
            interval_seconds=request.interval_seconds
        )
        return device.__dict__

    @app.get("/devices")
    def list_devices():
        return [d.__dict__ for d in device_service.list_devices()]

    @app.post("/devices/{device_id}/sync")
    def manual_sync(device_id: int):
        sync_service.sync_device(device_id)
        return {"status": "sync executed"}

    @app.get("/attendance")
    def get_attendance():
        return [r.__dict__ for r in attendance_repo.find_all()]

    return app



