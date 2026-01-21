from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import DeviceTable
from src.domain.models.device_config import DeviceConfig


class DeviceConfigRepositoryMySQL:

    def save(self, device: DeviceConfig) -> DeviceConfig:
        db = SessionLocal()
        try:
            model = DeviceTable(
                name=device.name,
                ip=device.ip,
                port=device.port,
                interval_seconds=device.interval_seconds,
                active=device.active
            )
            db.add(model)
            db.commit()
            db.refresh(model)

            device.device_id = model.id
            return device
        finally:
            db.close()

    def find_all(self):
        db = SessionLocal()
        try:
            rows = db.query(DeviceTable).all()
            return [
                DeviceConfig(
                    device_id=r.id,
                    name=r.name,
                    ip=r.ip,
                    port=r.port,
                    interval_seconds=r.interval_seconds,
                    active=r.active
                )
                for r in rows
            ]
        finally:
            db.close()

    def find_by_id(self, device_id: int):
        db = SessionLocal()
        try:
            r = db.query(DeviceTable).filter(DeviceTable.id == device_id).first()
            if not r:
                return None
            return DeviceConfig(
                device_id=r.id,
                name=r.name,
                ip=r.ip,
                port=r.port,
                interval_seconds=r.interval_seconds,
                active=r.active
            )
        finally:
            db.close()

    def find_active(self):
        db = SessionLocal()
        try:
            rows = (
                db.query(DeviceTable)
                .filter(DeviceTable.active == True)
                .all()
            )

            return [
                DeviceConfig(
                    device_id=r.id,
                    name=r.name,
                    ip=r.ip,
                    port=r.port,
                    interval_seconds=r.interval_seconds,
                    active=r.active
                )
                for r in rows
            ]
        finally:
            db.close()