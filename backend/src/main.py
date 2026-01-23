from src.infrastructure.api.attendance_api import create_app
from src.application.scheduler_service import SchedulerService
from src.application.device_sync_service import DeviceSyncService
from src.infrastructure.repositories.mysql.device_config_repository_mysql import DeviceConfigRepositoryMySQL
from src.infrastructure.repositories.mysql.attendance_repository_mysql import AttendanceRepositoryMySQL
from src.application.attendance_service import AttendanceService
from src.infrastructure.repositories.mysql.database import init_db
from src.application.user_service import UserService
from src.infrastructure.repositories.mysql.user_repository_mysql import UserRepositoryMySQL

from fastapi.middleware.cors import CORSMiddleware

init_db()

def main():
    device_repo = DeviceConfigRepositoryMySQL()
    attendance_repo = AttendanceRepositoryMySQL()
    user_repo = UserRepositoryMySQL()

    attendance_service = AttendanceService(attendance_repo)
    user_service= UserService(user_repo)
    sync_service = DeviceSyncService(device_repo, attendance_service, user_service)

    scheduler = SchedulerService(device_repo, sync_service)
    scheduler.start()

    app = create_app(
        device_repo=device_repo,
        attendance_repo=attendance_repo,
        sync_service=sync_service
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
