import os
import random
from datetime import datetime, timedelta
from typing import Callable, Iterable

from src.application.ports.biometric_device_repository import (
    BiometricAttendance,
    BiometricDeviceRepository,
    BiometricUser,
    DeviceRole,
)


class MockFingerprintDevice(BiometricDeviceRepository):
    """Deterministic full-snapshot adapter for local demos and tests."""

    def __init__(
        self,
        device_id: int,
        role: DeviceRole = DeviceRole.ENTRY,
        *,
        seed: int | None = None,
        burst_size: int = 5,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.device_id = device_id
        self.role = role
        self.burst_size = max(1, burst_size)
        self._clock = clock or datetime.now
        self._random = random.Random(seed if seed is not None else device_id)
        self._connected = False
        self._cycle = 0
        self._users = [
            BiometricUser(external_id="10000001", name="Juan Perez"),
            BiometricUser(external_id="10000002", name="Beatriz Gomez"),
            BiometricUser(external_id="10000003", name="Carlos Rodriguez"),
        ]
        self._attendance: list[BiometricAttendance] = []

    def connect(self) -> None:
        self._connected = True

    def fetch_users(self) -> Iterable[BiometricUser]:
        self._ensure_connected()
        self._cycle += 1
        if self._cycle % 2 == 0:
            external_id = f"100000{3 + self._cycle:02d}"
            self._users.append(
                BiometricUser(
                    external_id=external_id,
                    name=f"Demo Employee {self._cycle}",
                )
            )
        return tuple(self._users)

    def fetch_attendance(self) -> Iterable[BiometricAttendance]:
        self._ensure_connected()
        now = self._clock()
        role_offset = {
            DeviceRole.ENTRY: timedelta(hours=4),
            DeviceRole.CAFETERIA: timedelta(hours=2),
            DeviceRole.EXIT: timedelta(0),
        }[self.role]
        event_base = now - role_offset
        users = tuple(self._users)
        for offset in range(self.burst_size):
            user = users[(self._cycle + offset) % len(users)]
            event_time = event_base - timedelta(seconds=offset)
            self._attendance.append(
                BiometricAttendance(
                    user_external_id=user.external_id,
                    timestamp=event_time,
                )
            )
        # The real device returns the complete snapshot on every sync.
        return tuple(self._attendance)

    def disconnect(self) -> None:
        self._connected = False

    def _ensure_connected(self) -> None:
        if not self._connected:
            raise ConnectionError(
                f"Mock device {self.device_id} is not connected"
            )


def mock_device_from_environment(
    device_id: int,
    role: DeviceRole | None = None,
) -> MockFingerprintDevice:
    """Build a demo adapter using environment configuration."""

    role_name = os.getenv("MOCK_DEVICE_ROLE", DeviceRole.ENTRY.value)
    if role is None:
        try:
            role = DeviceRole(role_name.upper())
        except ValueError as error:
            raise ValueError(
                f"Unsupported MOCK_DEVICE_ROLE: {role_name}"
            ) from error

    return MockFingerprintDevice(
        device_id=device_id,
        role=role,
        seed=int(os.getenv("MOCK_SEED", str(device_id))),
        burst_size=int(os.getenv("MOCK_BURST_SIZE", "5")),
    )
