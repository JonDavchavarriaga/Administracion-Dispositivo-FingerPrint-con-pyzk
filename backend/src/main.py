from app.infrastructure.api.attendance_api import create_app
from app.application.scheduler_service import SchedulerService
from app.application.device_sync_service import DeviceSyncService
from app.infrastructure.repositories.device_config_repository import DeviceConfigRepository
from app.infrastructure.repositories.attendance_repository import AttendanceRepository
from app.application.attendance_service import AttendanceService


def main():
    device_repo = DeviceConfigRepository()
    attendance_repo = AttendanceRepository()

    attendance_service = AttendanceService(attendance_repo)
    sync_service = DeviceSyncService(device_repo, attendance_service)

    scheduler = SchedulerService(device_repo, sync_service)
    scheduler.start()

    app = create_app(
        device_repo=device_repo,
        attendance_repo=attendance_repo,
        sync_service=sync_service
    )
    return app


app = main()
