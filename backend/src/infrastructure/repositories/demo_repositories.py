from datetime import datetime

from src.domain.models.attendance_record import AttendanceRecord
from src.domain.models.cost_center import CostCenter
from src.domain.models.device_config import DeviceConfig
from src.domain.models.user import User


class DemoDeviceRepository:
    def __init__(self):
        self.devices = {
            1: DeviceConfig(1, "Demo Entry", "mock://entry", 4370, 300),
            2: DeviceConfig(2, "Demo Cafeteria", "mock://cafeteria", 4370, 300),
            3: DeviceConfig(3, "Demo Exit", "mock://exit", 4370, 300),
        }

    def save(self, device):
        device.device_id = max(self.devices, default=0) + 1
        self.devices[device.device_id] = device
        return device

    def find_all(self):
        return list(self.devices.values())

    def find_active(self):
        return [device for device in self.devices.values() if device.is_active]

    def find_by_id(self, device_id):
        return self.devices.get(device_id)

    def update(self, device):
        self.devices[device.device_id] = device
        return device

    def update_last_sync(self, device_id):
        self.devices[device_id].last_sync_at = datetime.utcnow()


class DemoUserRepository:
    def __init__(self):
        self.users = {}

    def save(self, user):
        user.user_id = len(self.users) + 1
        self.users[user.external_id] = user
        return user

    def find_by_external_id(self, external_id):
        return self.users.get(external_id)

    def find_all(self):
        return list(self.users.values())

    def find_by_id(self, user_id):
        return next((user for user in self.users.values() if user.user_id == user_id), None)

    def update(self, user):
        self.users[user.external_id] = user
        return user


class DemoAttendanceRepository:
    def __init__(self):
        self.records = {}

    def save(self, record):
        self.save_batch([record])

    def save_batch(self, records):
        for record in records:
            key = (record.device_id, record.user_external_id, record.timestamp)
            self.records[key] = record
        return len(records)

    def exists(self, user_id, device_id, timestamp):
        return any(
            record.user_id == user_id
            and record.device_id == device_id
            and record.timestamp == timestamp
            for record in self.records.values()
        )

    def find_last_timestamp(self, device_id):
        timestamps = [
            record.timestamp
            for record in self.records.values()
            if record.device_id == device_id
        ]
        return max(timestamps) if timestamps else None

    def find_all(self):
        return list(self.records.values())


class DemoCostCenterRepository:
    def __init__(self):
        self.cost_centers = {}

    def save(self, cost_center):
        cost_center.id = len(self.cost_centers) + 1
        self.cost_centers[cost_center.id] = cost_center
        return cost_center

    def find_all(self):
        return list(self.cost_centers.values())

    def find_by_id(self, cost_center_id):
        return self.cost_centers.get(cost_center_id)

    def update(self, cost_center):
        self.cost_centers[cost_center.id] = cost_center
        return cost_center

    def delete(self, cost_center_id):
        self.cost_centers.pop(cost_center_id, None)


class DemoUserDeviceRepository:
    def __init__(self):
        self.links = set()

    def link_user_to_device(self, user_id, device_id):
        self.links.add((user_id, device_id))
