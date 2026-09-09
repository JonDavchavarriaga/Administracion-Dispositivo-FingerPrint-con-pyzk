from src.domain.models.device_config import DeviceConfig
from datetime import datetime


class DeviceConfigService:

    def __init__(self, repository, sync_service):
        self.repository = repository
        self.sync_service = sync_service

    def create_device(self, name, ip, port, interval_seconds):
        device = DeviceConfig(
            device_id=None,
            name=name,
            ip=ip,
            port=port,
            interval_seconds=interval_seconds,
            is_active=True,
            last_sync_at=None
        )
        saved = self.repository.save(device)

        try:
            self.sync_service.sync_device(saved.device_id)
        except Exception:
            pass

        return saved

    def list_devices(self):
        return self.repository.find_all()

    def update_device(self, device_id, **fields):
        device = self.repository.find_by_id(device_id)
        if not device:
            raise ValueError("Device not found")

        for k, v in fields.items():
            setattr(device, k, v)

        return self.repository.update(device)

    def activate_device(self, device_id: int, is_active: bool):
        device = self.repository.find_by_id(device_id)
        if not device:
            raise ValueError("Device not found")

        device.is_active = is_active
        return self.repository.update(device)

def deactivate_device(self, device_id: int):
    device = self.repository.find_by_id(device_id)
    if not device:
        raise ValueError("Device not found")

    device.is_active = False
    return self.repository.update(device)
