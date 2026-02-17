from src.infrastructure.repositories.mysql.models import UserDeviceTable
from src.infrastructure.repositories.mysql.database import SessionLocal

class UserDeviceRepositoryMySQL:

    def link_user_to_device(self, user_id: int, device_id: int):
        db = SessionLocal()
        try:
            exists = (
                db.query(UserDeviceTable)
                .filter_by(user_id=user_id, device_id=device_id)
                .first()
            )

            if not exists:
                db.add(UserDeviceTable(
                    user_id=user_id,
                    device_id=device_id
                ))
                db.commit()
        finally:
            db.close()