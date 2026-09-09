import sys
from pathlib import Path

# Add the backend directory to the Python path.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.infrastructure.devices.zk_device import ZKTecoBiometricDeviceRepository
from src.infrastructure.repositories.mysql.device_config_repository_mysql import DeviceConfigRepositoryMySQL


def debug_devices():

    repo = DeviceConfigRepositoryMySQL()

    devices = repo.find_active()

    print("\n==============================")
    print(" BIOMETRIC DEVICE DIAGNOSTICS ")
    print("==============================\n")

    if not devices:
        print("No active devices found in the database")
        return

    for device in devices:
        print(f"Device ID: {device.device_id}")
        print(f"Name: {device.name}")
        print(f"Connection: {device.ip}:{device.port}")
        print(f"Interval: {device.interval_seconds}s")
        print("Connecting...")

        zk = ZKTecoBiometricDeviceRepository(
            ip=device.ip,
            port=device.port
        )

        try:
            zk.connect()
            print("Connected")

            users = tuple(zk.fetch_users())
            print(f"Users found: {len(users)}")

            records = tuple(zk.fetch_attendance())
            print(f"Attendance records found: {len(records)}")

            if records:
                print(f"Primera marcación: {records[0].timestamp}")
                print(f"Última marcación: {records[-1].timestamp}")
            else:
                print("The device has no attendance records")

        except Exception as e:
            print(f"ERROR: {e}")

        finally:
            try:
                zk.disconnect()
                print("Disconnected")
            except:
                pass

        print("\n--------------------------------\n")

    print("END OF DIAGNOSTICS\n")


if __name__ == "__main__":
    debug_devices()
