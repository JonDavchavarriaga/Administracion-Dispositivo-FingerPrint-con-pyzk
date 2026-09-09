from src.domain.models.attendance_record import AttendanceRecord
from datetime import datetime


class AttendanceService:
    def __init__(self, repository):
        self.repository = repository

    def process_record(
        self,
        *,
        user_id: int,
        user_external_id: str,
        device_id: int,
        timestamp,
    ):
        """
        Guarda la marcación solo si no existe
        """

        record = AttendanceRecord(
            user_id=user_id,
            user_external_id=user_external_id,
            device_id=device_id,
            timestamp=timestamp,
            created_at=datetime.now(),
        )

        self.repository.save(record)

    def process_records(self, records):
        return self.repository.save_batch(records)

    def get_last_timestamp(self, device_id: int):
        return self.repository.find_last_timestamp(device_id)
