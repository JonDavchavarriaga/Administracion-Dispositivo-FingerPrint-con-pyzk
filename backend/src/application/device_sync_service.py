from app.infrastructure.devices.zk_device import ZKFingerprintDevice


class DeviceSyncService:
    def __init__(self, device_repo, attendance_service):
        self.device_repo = device_repo
        self.attendance_service = attendance_service

    def sync_device(self, device_id: int):
        device = self.device_repo.find_by_id(device_id)
        if not device or not device.active:
            return

        zk_device = ZKFingerprintDevice(
            ip=device.ip,
            port=device.port
        )

        try:
            zk_device.connect()
            records = zk_device.get_attendance()

            for raw_record in records:
                self.attendance_service.process_record(
                    raw_record,
                    device.device_id
                )

        finally:
            zk_device.disconnect()

