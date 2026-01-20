class AttendanceRepository:
    def __init__(self):
        self.records = []

    def save(self, record):
        self.records.append(record)

    def find_all(self):
        return self.records

    def get_last_timestamp_by_device(self, device_id: int):
        device_records = [
            r for r in self.records if r.device_id == device_id
        ]

        if not device_records:
            return None

        return max(r.timestamp for r in device_records)
