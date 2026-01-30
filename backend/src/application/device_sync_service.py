from src.application.user_service import UserService
from src.infrastructure.devices.zk_device import ZKFingerprintDevice


class DeviceSyncService:

    def __init__(self, device_repo, attendance_service, user_service):
        self.device_repo = device_repo
        self.attendance_service = attendance_service
        self.user_service = user_service

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

            # ========= Usuarios ========
            users = zk_device.get_users()

            user_map = {}
            for u in users:
                user = self.user_service.find_or_create_from_device(
                    external_id=str(u["user_id"]),
                    name=u["name"]
                )
                user_map[str(u["user_id"])] = user

            #========== Marcaciones =======
            records = zk_device.get_attendance()

            for r in records:
                user = user_map.get(str(r["user_id"]))
                if not user:
                    continue

                self.attendance_service.process_record(
                    user_id=user.user_id,
                    device_id=device.device_id,
                    timestamp=r["timestamp"]
                )
        finally:
            zk_device.disconnect()
