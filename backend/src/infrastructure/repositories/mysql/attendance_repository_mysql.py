from src.application.ports.attendance_repository import AttendanceRepository
from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import AttendanceTable
from src.domain.models.attendance_record import AttendanceRecord


class AttendanceRepositoryMySQL(AttendanceRepository):

    def save(self, record: AttendanceRecord):
        db = SessionLocal()
        try:
            model = AttendanceTable(
                user_id=record.user_id,
                device_id=record.device_id,
                timestamp=record.timestamp,
                created_at=record.created_at
            )
            db.add(model)
            db.commit()
        finally:
            db.close()

    def exists(self, user_id: int, device_id: int, timestamp) -> bool:
        db = SessionLocal()
        try:
            return (
                db.query(AttendanceTable)
                .filter(
                    AttendanceTable.user_id == user_id,
                    AttendanceTable.device_id == device_id,
                    AttendanceTable.timestamp == timestamp
                )
                .first()
                is not None
            )
        finally:
            db.close()
