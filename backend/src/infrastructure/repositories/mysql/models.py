from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class DeviceTable(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    ip = Column(String(50))
    port = Column(Integer, default=4370)
    interval_seconds = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)


class AttendanceTable(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    device_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(50), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    active = Column(Boolean, default=True)