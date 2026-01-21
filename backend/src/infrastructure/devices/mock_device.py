from datetime import datetime
from random import choice

from src.infrastructure.devices.base_device import FingerprintDevice

class MockFingerprintDevice(FingerprintDevice):
    """"
    Dispositivo de Huellas Digitales Simulado para Pruebas
    """
    def __init__(self,device_id):
        self.device_id = device_id # Identificador del Dispositivo Unico
        self.connected = False
        self.users = [
            {"user_id": 1, "name": "Juan Perez "},
            {"user_id": 2, "name": "Beatriz Gomez"},
        ]
        self.attendance= [] # Memoria Interna de Registros

    def connect(self):
        self.connected = True
        print(f"[MockFingerprintDevice {self.device_id}] Conectado.") #Simula TCP/IP Exitosa
        
    def get_users(self):
        return self.users
    
    def get_attendance(self):
        user= choice(self.users)
        record= {
            "user_id": user["user_id"],
            "device_id": self.device_id,
            "timestamp": datetime.now(),
        }    
        self.attendance.append(record)
        return [record]
    
    def disconnect(self):
        self.connected = False
        print(f"[MockFingerprintDevice {self.device_id}] Desconectado.")