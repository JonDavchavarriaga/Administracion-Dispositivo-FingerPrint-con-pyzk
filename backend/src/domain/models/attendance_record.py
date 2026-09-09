from datetime import datetime

class AttendanceRecord:
    def __init__(
        self,
        user_id: int,
        user_external_id: str,
        device_id: int,
        timestamp: datetime,
        created_at: datetime
    ):
        self.user_id = user_id
        self.user_external_id = user_external_id
        self.device_id = device_id
        self.timestamp = timestamp
        self.created_at = created_at
