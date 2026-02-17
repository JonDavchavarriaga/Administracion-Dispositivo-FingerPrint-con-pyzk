from abc import ABC, abstractmethod

class UserDeviceRepository(ABC):
    @abstractmethod
    def link_user_to_device(self, user_id: int, device_id: int):
        """
        Vincula un usuario a un dispositivo.
        """
        pass