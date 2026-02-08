import time
import threading
from datetime import datetime, timedelta


class SchedulerService:

    def __init__(self, device_repo, sync_service):
        self.device_repo = device_repo
        self.sync_service = sync_service
        self._running = False

    def start(self):
        if self._running:
            return

        self._running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        while self._running:
            now = datetime.now()

            devices = self.device_repo.find_active()

            for device in devices:
                # Nunca sincronizado → sync inmediato
                if device.last_sync_at is None:
                    self.sync_service.sync_device(device.device_id)
                    continue

                next_sync = device.last_sync_at + timedelta(
                    seconds=device.interval_seconds
                )

                if now >= next_sync:
                    self.sync_service.sync_device(device.device_id)

            # Tick corto (scheduler liviano)
            time.sleep(10)

    def stop(self):
        self._running = False
