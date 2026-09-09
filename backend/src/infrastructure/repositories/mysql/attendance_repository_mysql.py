from src.application.ports.attendance_repository import AttendanceRepository
from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import AttendanceTable
from src.domain.models.attendance_record import AttendanceRecord
from sqlalchemy.dialects.mysql import insert


class AttendanceRepositoryMySQL(AttendanceRepository):

    def save(self, record: AttendanceRecord):
        db = SessionLocal()
        try:
            model = AttendanceTable(
                user_id=record.user_id,
                user_external_id=record.user_external_id,
                device_id=record.device_id,
                timestamp=record.timestamp,
                created_at=record.created_at
            )
            db.add(model)
            db.commit()
        finally:
            db.close()

    def save_batch(self, records: list[AttendanceRecord]) -> int:
        if not records:
            return 0
        db = SessionLocal()
        try:
            inserted = 0
            for offset in range(0, len(records), 500):
                chunk = records[offset:offset + 500]
                statement = insert(AttendanceTable).values(
                    [
                        {
                            "user_id": record.user_id,
                            "user_external_id": record.user_external_id,
                            "device_id": record.device_id,
                            "timestamp": record.timestamp,
                            "created_at": record.created_at,
                        }
                        for record in chunk
                    ]
                )
                statement = statement.on_duplicate_key_update(
                    id=AttendanceTable.id
                )
                result = db.execute(statement)
                inserted += result.rowcount
            db.commit()
            return inserted
        except Exception:
            db.rollback()
            raise
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

    def find_last_timestamp(self, device_id: int):
        db = SessionLocal()
        try:
            result = (
                db.query(AttendanceTable.timestamp)
                .filter(AttendanceTable.device_id == device_id)
                .order_by(AttendanceTable.timestamp.desc())
                .first()
            )
            return result[0] if result else None
        finally:
            db.close()
