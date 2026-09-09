from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Iterable


class DeviceRole(StrEnum):
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    CAFETERIA = "CAFETERIA"


@dataclass(frozen=True)
class BiometricUser:
    external_id: str
    name: str


@dataclass(frozen=True)
class BiometricAttendance:
    user_external_id: str
    timestamp: datetime


class BiometricDeviceRepository(ABC):
    """Port for reading a biometric device without exposing its SDK."""

    @abstractmethod
    def connect(self) -> None:
        """Open the device connection."""

    @abstractmethod
    def fetch_users(self) -> Iterable[BiometricUser]:
        """Return the complete user snapshot from the device."""

    @abstractmethod
    def fetch_attendance(self) -> Iterable[BiometricAttendance]:
        """Return the complete attendance snapshot from the device."""

    @abstractmethod
    def disconnect(self) -> None:
        """Close the device connection and release resources."""
