class DeviceConfig:
    def __init__(
        self,
        device_id,
        name,
        ip,
        port,
        interval_seconds,
        is_active=True,
        last_sync_at=None
    ):
        self.device_id = device_id
        self.name = name
        self.ip = ip
        self.port = port
        self.interval_seconds = interval_seconds
        self.is_active = is_active
        self.last_sync_at = last_sync_at