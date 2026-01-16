class DeviceConfig:
    def __init__(
        self,
        device_id,
        name,
        ip,
        port,
        interval_seconds,
        active=True
    ):
        self.device_id = device_id
        self.name = name
        self.ip = ip
        self.port = port
        self.interval_seconds = interval_seconds
        self.active = active
