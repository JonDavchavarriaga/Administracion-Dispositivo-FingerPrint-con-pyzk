from src.infrastructure.repositories.mysql.models import UserDeviceTable
from src.infrastructure.repositories.mysql.database import SessionLocal

class UserDeviceRepositoryMySQL:

    def link_user_to_device(self, user_id: int, device_id: int):
        db = SessionLocal()
        try:
            db.execute(
                UserDeviceTable.__table__.insert().prefix_with("IGNORE"),
                {"user_id": user_id, "device_id": device_id}
            )
            db.commit()
        finally:
            db.close()