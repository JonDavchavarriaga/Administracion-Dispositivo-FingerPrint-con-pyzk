from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class CostCenterTable(Base):
    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    users = relationship("UserTable", back_populates="cost_center")

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id", ondelete="SET NULL"), nullable=True)
    is_active = Column(Boolean, default=True)

    cost_center = relationship("CostCenterTable", back_populates="users")

class DeviceTable(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ip = Column(String(50), nullable=False)
    port = Column(Integer, default=4370)
    interval_seconds = Column(Integer, nullable=False, default=60)
    is_active = Column(Boolean, default=True)
    last_sync_at = Column(DateTime, nullable=True)


class UserDeviceTable(Base):
    __tablename__ = "user_devices"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="CASCADE"), primary_key=True)

class AttendanceTable(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="RESTRICT"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
