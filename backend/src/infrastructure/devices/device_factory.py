import os

from src.application.ports.biometric_device_repository import (
    BiometricDeviceRepository,
    DeviceRole,
)
from src.domain.models.device_config import DeviceConfig
from src.infrastructure.devices.mock_device import (
    MockFingerprintDevice,
    mock_device_from_environment,
)

_mock_devices: dict[int, MockFingerprintDevice] = {}


def build_biometric_device(
    device: DeviceConfig,
) -> BiometricDeviceRepository:
    """Build the adapter selected by deployment configuration."""

    mock_mode = os.getenv("MOCK_MODE", "False").lower() == "true"
    if mock_mode:
        role = _role_from_device_name(device.name)
        if device.device_id not in _mock_devices:
            _mock_devices[device.device_id] = mock_device_from_environment(
                device.device_id,
                role,
            )
        return _mock_devices[device.device_id]
    from src.infrastructure.devices.zk_device import (
        ZKTecoBiometricDeviceRepository,
    )

    return ZKTecoBiometricDeviceRepository(
        ip=device.ip,
        port=device.port,
    )


def _role_from_device_name(name: str) -> DeviceRole:
    normalized_name = name.upper()
    role_aliases = {
        DeviceRole.ENTRY: ("ENTRY", "ENTRADA"),
        DeviceRole.EXIT: ("EXIT", "SALIDA"),
        DeviceRole.CAFETERIA: ("CAFETERIA", "CAFETERÍA", "COMEDOR", "MEAL"),
    }
    for role, aliases in role_aliases.items():
        if any(alias in normalized_name for alias in aliases):
            return role
    return DeviceRole.ENTRY
