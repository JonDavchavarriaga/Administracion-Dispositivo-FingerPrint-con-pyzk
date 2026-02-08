from datetime import datetime
from src.application.ports.device_config_repository import DeviceConfigRepository
from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import DeviceTable
from src.domain.models.device_config import DeviceConfig


class DeviceConfigRepositoryMySQL(DeviceConfigRepository):

    def save(self, device: DeviceConfig) -> DeviceConfig:
        db = SessionLocal()
        try:
            model = DeviceTable(
                name=device.name,
                ip=device.ip,
                port=device.port,
                interval_seconds=device.interval_seconds,
                is_active=device.is_active,
                last_sync_at=device.last_sync_at
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
            return [
                self._to_domain(r)
                for r in db.query(DeviceTable).all()
            ]
        finally:
            db.close()

    def find_active(self):
        db = SessionLocal()
        try:
            return [
                self._to_domain(r)
                for r in db.query(DeviceTable)
                .filter(DeviceTable.is_active == True)
                .all()
            ]
        finally:
            db.close()

    def update(self, device: DeviceConfig) -> DeviceConfig:
        db = SessionLocal()
        try:
            model = db.query(DeviceTable).get(device.device_id)
            if not model:
                raise ValueError("Device not found")

            model.name = device.name
            model.ip = device.ip
            model.port = device.port
            model.interval_seconds = device.interval_seconds
            model.is_active = device.is_active
            model.last_sync_at = device.last_sync_at

            db.commit()
            return device
        finally:
            db.close()

    def find_by_id(self, device_id: int):
        db = SessionLocal()
        try:
            r = db.query(DeviceTable).filter(DeviceTable.id == device_id).first()
            return self._to_domain(r) if r else None
        finally:
            db.close()

    def update_last_sync(self, device_id: int):
        db = SessionLocal()
        try:
            device = db.query(DeviceTable).get(device_id)
            if device:
                device.last_sync_at = datetime.now()
                db.commit()
        finally:
            db.close()

    def deactivate(self, device_id: int):
        db = SessionLocal()
        try:
            model = db.query(DeviceTable).get(device_id)
            if not model:
                raise ValueError("Device not found")

            db.delete(model)
            db.commit()
        finally:
            db.close()

    def _to_domain(self, r: DeviceTable) -> DeviceConfig:
        return DeviceConfig(
            device_id=r.id,
            name=r.name,
            ip=r.ip,
            port=r.port,
            interval_seconds=r.interval_seconds,
            is_active=r.is_active,
            last_sync_at=r.last_sync_at
        )

