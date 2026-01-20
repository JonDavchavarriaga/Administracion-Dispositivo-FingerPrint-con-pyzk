from app.domain.models.device_config import DeviceConfig


class DeviceConfigService:
    def __init__(self, repository):
        self.repository = repository

    def register_device(self, name, ip, port, interval_seconds):
        device = DeviceConfig(
            device_id=None,
            name=name,
            ip=ip,
            port=port,
            interval_seconds=interval_seconds,
            active=True
        )
        return self.repository.save(device)

    def list_devices(self):
        return self.repository.find_all()
