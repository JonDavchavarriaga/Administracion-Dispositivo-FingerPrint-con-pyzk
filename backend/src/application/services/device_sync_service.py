from collections.abc import Callable

from src.application.ports.biometric_device_repository import (
    BiometricDeviceRepository,
)


class DeviceSyncService:
    def __init__(
        self,
        device_repo,
        attendance_service,
        user_service,
        user_device_repo,
        device_factory: Callable[[object], BiometricDeviceRepository] | None = None,
    ):
        self.device_repo = device_repo
        self.attendance_service = attendance_service
        self.user_service = user_service
        self.user_device_repo = user_device_repo
        self.device_factory = device_factory

    def sync_device(self, device_id: int):
        device = self.device_repo.find_by_id(device_id)
        if not device or not device.is_active:
            raise ValueError(f"Device {device_id} was not found or is inactive")

        if self.device_factory is None:
            raise RuntimeError("No biometric device factory has been configured")

        biometric_device: BiometricDeviceRepository = self.device_factory(device)
        try:
            biometric_device.connect()
            users = tuple(biometric_device.fetch_users())
            user_map = {}

            for biometric_user in users:
                user = self.user_service.find_or_create_from_device(
                    external_id=biometric_user.external_id,
                    name=biometric_user.name,
                )
                self.user_device_repo.link_user_to_device(
                    user_id=user.user_id,
                    device_id=device.device_id,
                )
                user_map[biometric_user.external_id] = user

            # The hardware returns a complete snapshot; persistence becomes
            # idempotent through the repository unique constraint.
            records = tuple(biometric_device.fetch_attendance())
            for record in records:
                user = user_map.get(record.user_external_id)
                if user is None:
                    continue
                self.attendance_service.process_record(
                    user_id=user.user_id,
                    device_id=device.device_id,
                    timestamp=record.timestamp,
                )

            self.device_repo.update_last_sync(device.device_id)
            return {
                "device_id": device.device_id,
                "users": len(users),
                "attendance_records": len(records),
            }
        finally:
            biometric_device.disconnect()

    def sync_all(self):
        return [
            self.sync_device(device.device_id)
            for device in self.device_repo.find_active()
        ]
