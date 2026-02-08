from src.infrastructure.api.attendance_api import create_app
from src.application.sevices.scheduler_service import SchedulerService
from src.application.sevices.device_sync_service import DeviceSyncService
from src.application.sevices.attendance_service import AttendanceService
from src.application.sevices.user_service import UserService
from src.application.sevices.cost_center_service import CostCenterService

from src.infrastructure.repositories.mysql.device_config_repository_mysql import DeviceConfigRepositoryMySQL
from src.infrastructure.repositories.mysql.attendance_repository_mysql import AttendanceRepositoryMySQL
from src.infrastructure.repositories.mysql.user_repository_mysql import UserRepositoryMySQL
from src.infrastructure.repositories.mysql.cost_center_repository_mysql import CostCenterRepositoryMySQL

from src.infrastructure.repositories.mysql.database import init_db
from fastapi.middleware.cors import CORSMiddleware

init_db()

def main():
    # ===== Repositories =====
    device_repo = DeviceConfigRepositoryMySQL()
    attendance_repo = AttendanceRepositoryMySQL()
    user_repo = UserRepositoryMySQL()
    cost_center_repo = CostCenterRepositoryMySQL()

    # ===== Services =====
    attendance_service = AttendanceService(attendance_repo)
    user_service = UserService(user_repo)

    sync_service = DeviceSyncService(
        device_repo=device_repo,
        attendance_service=attendance_service,
        user_service=user_service
    )

    # ===== Scheduler =====
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
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = main()
