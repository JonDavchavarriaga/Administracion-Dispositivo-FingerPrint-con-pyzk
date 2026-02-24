from src.domain.models.attendance_record import AttendanceRecord
from datetime import datetime


class AttendanceService:
    def __init__(self, repository):
        self.repository = repository

    def process_record(self, *, user_id: int, device_id: int, timestamp):
        """
        Guarda la marcación solo si no existe
        """

        if self.repository.exists(user_id, device_id, timestamp):
            return

        record = AttendanceRecord(
            user_id=user_id,
            device_id=device_id,
            timestamp=timestamp,
            created_at=datetime.now(),
        )

        self.repository.save(record)

    def get_last_timestamp(self, device_id: int):
        return self.repository.find_last_timestamp(device_id)

