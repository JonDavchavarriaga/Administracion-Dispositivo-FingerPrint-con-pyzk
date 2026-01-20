import time
import threading

class SchedulerService:
    def __init__(self, device_repo, sync_service):
        self.device_repo = device_repo
        self.sync_service = sync_service

    def start(self):
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        while True:
            devices = self.device_repo.find_active()
            for device in devices:
                self.sync_service.sync_device(device.device_id)

            time.sleep(300)  # 5 minutos
