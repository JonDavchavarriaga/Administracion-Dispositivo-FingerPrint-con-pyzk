from abc import ABC, abstractmethod

class FingerprintDevice(ABC):
    """
    Contrato que Todo Huellero Debe Cumplir
    """
    @abstractmethod
    def connect(self):
        """
        Conecta al dispositivo de huellas digitales.
        :return: True si la conexión fue exitosa, False en caso contrario.
        """
        pass
    
    @abstractmethod
    def get_users(self):
        """
        Obtiene la lista de usuarios almacenados en el dispositivo.
        :return: Lista de usuarios.
        """
        pass
    
    @abstractmethod
    def get_attendance(self):
        """
        Obtiene los registros de asistencia del dispositivo.
        :return: Lista de registros de asistencia.
        """
        pass
    
    @abstractmethod
    def disconnect(self):
        """
        Cierre de Conexión
        """
        pass