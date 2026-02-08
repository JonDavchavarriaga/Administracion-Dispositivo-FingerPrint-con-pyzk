from abc import ABC, abstractmethod
from src.domain.models.device_config import DeviceConfig


class DeviceConfigRepository(ABC):

    @abstractmethod
    def save(self, device: DeviceConfig) -> DeviceConfig:
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_active(self):
        pass

    @abstractmethod
    def find_by_id(self, device_id: int):
        pass

    @abstractmethod
    def update_last_sync(self, device_id: int):
        pass

    @abstractmethod
    def deactivate(self, device_id: int):
        pass