from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import AttendanceTable
from src.domain.models.attendance_record import AttendanceRecord


class AttendanceRepositoryMySQL:

    def save(self, attendance: AttendanceRecord):
        db = SessionLocal()
        try:
            model = AttendanceTable(
                user_id=attendance.user_id,
                device_id=attendance.device_id,
                timestamp=attendance.timestamp
            )
            db.add(model)
            db.commit()
        finally:
            db.close()

    def exists(self, user_id: int, device_id: int, timestamp):
        db = SessionLocal()
        try:
            return db.query(AttendanceTable).filter(
                AttendanceTable.user_id == user_id,
                AttendanceTable.device_id == device_id,
                AttendanceTable.timestamp == timestamp
            ).first() is not None
        finally:
            db.close()

    def find_all(self):
        db = SessionLocal()
        try:
            records = db.query(AttendanceTable).all()
            return [
                AttendanceRecord(
                    user_id=r.user_id,
                    device_id=r.device_id,
                    timestamp=r.timestamp
                )
                for r in records
            ]
        finally:
            db.close()

