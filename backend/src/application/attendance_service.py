from app.domain.models.attendance_record import AttendanceRecord


class AttendanceService:
    def __init__(self, repository):
        self.repository = repository

    def process_record(self, raw_record, device_id: int):
        last_timestamp = self.repository.get_last_timestamp_by_device(device_id)

        if last_timestamp and raw_record.timestamp <= last_timestamp:
            return

        record = AttendanceRecord(
            user_id=raw_record.user_id,
            device_id=device_id,
            timestamp=raw_record.timestamp
        )

        self.repository.save(record)
