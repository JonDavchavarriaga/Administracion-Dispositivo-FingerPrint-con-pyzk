from src.infrastructure.api.attendance_api import create_app
from src.application.services.scheduler_service import SchedulerService
from src.application.services.device_sync_service import DeviceSyncService
from src.application.services.attendance_service import AttendanceService
from src.application.services.user_service import UserService
from src.application.services.cost_center_service import CostCenterService

from src.infrastructure.repositories.mysql.device_config_repository_mysql import DeviceConfigRepositoryMySQL
from src.infrastructure.repositories.mysql.attendance_repository_mysql import AttendanceRepositoryMySQL
from src.infrastructure.repositories.mysql.user_repository_mysql import UserRepositoryMySQL
from src.infrastructure.repositories.mysql.cost_center_repository_mysql import CostCenterRepositoryMySQL
from src.infrastructure.repositories.mysql.user_device_repository_mysql import UserDeviceRepositoryMySQL
from src.infrastructure.devices.device_factory import build_biometric_device

from fastapi.middleware.cors import CORSMiddleware

def main():
    # ===== Repositories =====
    device_repo = DeviceConfigRepositoryMySQL()
    attendance_repo = AttendanceRepositoryMySQL()
    user_repo = UserRepositoryMySQL()
    cost_center_repo = CostCenterRepositoryMySQL()
    user_device_repo = UserDeviceRepositoryMySQL()
    # ===== Services =====
    attendance_service = AttendanceService(attendance_repo)
    user_service = UserService(user_repo)

    sync_service = DeviceSyncService(
        device_repo=device_repo,
        attendance_service=attendance_service,
        user_service=user_service,
        user_device_repo=user_device_repo,
        device_factory=build_biometric_device,
    )

    # ===== Scheduler =====
    if os.getenv("ENABLE_LEGACY_SCHEDULER", "False").lower() == "true":
        scheduler = SchedulerService(device_repo, sync_service)
        scheduler.start()

    # ===== API =====
    app = create_app(
        device_repo=device_repo,
        attendance_repo=attendance_repo,
        sync_service=sync_service,
        user_repo=user_repo,
        cost_center_repo=cost_center_repo
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS",
                "http://localhost:5173",
            ).split(",")
            if origin.strip()
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "ok", "demo_mode": os.getenv("MOCK_MODE", "False").lower() == "true"}

    return app


app = main()
import os
