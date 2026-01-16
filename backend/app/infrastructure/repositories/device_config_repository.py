class DeviceConfigRepository:
    def __init__(self):
        self.devices = []
        self._id_counter = 1

    def save(self, device):
        device.device_id = self._id_counter
        self._id_counter += 1
        self.devices.append(device)
        return device

    def find_all(self):
        return self.devices

    def find_active(self):
        return [d for d in self.devices if d.active]

    def find_by_id(self, device_id: int):
        for device in self.devices:
            if device.device_id == device_id:
                return device
        return None
