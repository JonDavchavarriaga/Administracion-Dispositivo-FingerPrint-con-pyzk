import sys
from pathlib import Path

# agrega la carpeta backend al path de Python
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.infrastructure.devices.zk_device import ZKFingerprintDevice
from src.infrastructure.repositories.mysql.device_config_repository_mysql import DeviceConfigRepositoryMySQL


def debug_devices():

    repo = DeviceConfigRepositoryMySQL()

    devices = repo.find_active()

    print("\n==============================")
    print(" DIAGNÓSTICO DE HUELEROS ")
    print("==============================\n")

    if not devices:
        print("No hay dispositivos activos en base de datos")
        return

    for device in devices:
        print(f"Device ID: {device.device_id}")
        print(f"Nombre: {device.name}")
        print(f"Conexión: {device.ip}:{device.port}")
        print(f"Intervalo: {device.interval_seconds}s")
        print("Conectando...")

        zk = ZKFingerprintDevice(
            ip=device.ip,
            port=device.port
        )

        try:
            zk.connect()
            print("✔ Conectado")

            users = zk.get_users()
            print(f"Usuarios encontrados: {len(users)}")

            records = zk.get_attendance()
            print(f"Marcaciones encontradas: {len(records)}")

            if records:
                print(f"Primera marcación: {records[0]['timestamp']}")
                print(f"Última marcación: {records[-1]['timestamp']}")
            else:
                print("⚠ El dispositivo no tiene marcaciones")

        except Exception as e:
            print(f"✖ ERROR: {e}")

        finally:
            try:
                zk.disconnect()
                print("Desconectado")
            except:
                pass

        print("\n--------------------------------\n")

    print("FIN DEL DIAGNÓSTICO\n")


if __name__ == "__main__":
    debug_devices()
