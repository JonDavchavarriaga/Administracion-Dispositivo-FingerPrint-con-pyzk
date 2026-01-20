from zk import ZK
from app.infrastructure.devices.base_device import FingerprintDevice


class ZKFingerprintDevice(FingerprintDevice):
    def __init__(self, ip, port=4370, timeout=5):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.conn = None

    def connect(self):
        zk = ZK(
            self.ip,
            port=self.port,
            timeout=self.timeout,
            password=0,
            force_udp=False,
            ommit_ping=False
        )
        self.conn = zk.connect()
        print(f"[ZK] Conectado a {self.ip}")

    def get_users(self):
        users = self.conn.get_users()
        return [
            {
                "user_id": u.user_id,
                "name": u.name
            }
            for u in users
        ]

    def get_attendance(self):
        records = self.conn.get_attendance()
        return [
            {
                "user_id": r.user_id,
                "device_id": self.ip,
                "timestamp": r.timestamp
            }
            for r in records
        ]

    def disconnect(self):
        if self.conn:
            self.conn.disconnect()
            print(f"[ZK] Desconectado de {self.ip}")
            