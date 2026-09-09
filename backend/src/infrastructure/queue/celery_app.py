import os

from celery import Celery

celery_app = Celery(
    "attendance_platform",
    broker=os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
)
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    beat_schedule={
        "sync-active-devices": {
            "task": "src.infrastructure.queue.celery_app.synchronize_all_devices",
            "schedule": 300.0,
        },
    },
)


@celery_app.task(
    bind=True,
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=5,
)
def synchronize_device(self, device_id: int):
    from src.application.services.attendance_service import AttendanceService
    from src.application.services.device_sync_service import DeviceSyncService
    from src.application.services.user_service import UserService
    from src.infrastructure.devices.device_factory import build_biometric_device
    from src.infrastructure.repositories.mysql.attendance_repository_mysql import (
        AttendanceRepositoryMySQL,
    )
    from src.infrastructure.repositories.mysql.device_config_repository_mysql import (
        DeviceConfigRepositoryMySQL,
    )
    from src.infrastructure.repositories.mysql.user_device_repository_mysql import (
        UserDeviceRepositoryMySQL,
    )
    from src.infrastructure.repositories.mysql.user_repository_mysql import (
        UserRepositoryMySQL,
    )

    attendance_repository = AttendanceRepositoryMySQL()
    service = DeviceSyncService(
        device_repo=DeviceConfigRepositoryMySQL(),
        attendance_service=AttendanceService(attendance_repository),
        user_service=UserService(UserRepositoryMySQL()),
        user_device_repo=UserDeviceRepositoryMySQL(),
        device_factory=build_biometric_device,
    )
    return service.sync_device(device_id)


@celery_app.task
def synchronize_all_devices():
    from src.infrastructure.repositories.mysql.device_config_repository_mysql import (
        DeviceConfigRepositoryMySQL,
    )

    task_ids = []
    for device in DeviceConfigRepositoryMySQL().find_active():
        task_ids.append(synchronize_device.delay(device.device_id).id)
    return task_ids
