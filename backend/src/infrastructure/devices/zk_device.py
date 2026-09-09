from typing import Iterable

from src.application.ports.biometric_device_repository import (
    BiometricAttendance,
    BiometricDeviceRepository,
    BiometricUser,
)


class ZKTecoBiometricDeviceRepository(BiometricDeviceRepository):
    """ZKTeco adapter; the pyzk dependency is intentionally isolated here."""

    def __init__(self, ip: str, port: int = 4370, timeout: int = 5) -> None:
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self._connection = None

    def connect(self) -> None:
        from zk import ZK

        client = ZK(
            self.ip,
            port=self.port,
            timeout=self.timeout,
            force_udp=True,
            ommit_ping=True,
        )
        self._connection = client.connect()

    def fetch_users(self) -> Iterable[BiometricUser]:
        connection = self._require_connection()
        return tuple(
            BiometricUser(external_id=str(user.user_id), name=user.name)
            for user in connection.get_users()
        )

    def fetch_attendance(self) -> Iterable[BiometricAttendance]:
        connection = self._require_connection()
        return tuple(
            BiometricAttendance(
                user_external_id=str(record.user_id),
                timestamp=record.timestamp,
            )
            for record in connection.get_attendance()
        )

    def disconnect(self) -> None:
        if self._connection is not None:
            self._connection.disconnect()
            self._connection = None

    def _require_connection(self):
        if self._connection is None:
            raise ConnectionError(f"ZKTeco device {self.ip} is not connected")
        return self._connection
