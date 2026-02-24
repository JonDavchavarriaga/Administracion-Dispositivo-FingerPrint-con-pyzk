from abc import ABC, abstractmethod
from src.domain.models.attendance_record import AttendanceRecord


class AttendanceRepository(ABC):

    @abstractmethod
    def save(self, record: AttendanceRecord):
        pass

    @abstractmethod
    def exists(self, user_id: int, device_id: int, timestamp) -> bool:
        pass

    @abstractmethod
    def find_last_timestamp(self,device_id: int):
        pass