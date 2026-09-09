import time
import threading
from datetime import datetime, timedelta


class SchedulerService:

    def __init__(self, device_repo, sync_service):
        self.device_repo = device_repo
        self.sync_service = sync_service
        self._running = False
        self._device_locks = {}

    def start(self):
        if self._running:
            print("[SCHEDULER] Ya estaba en ejecución")
            return

        print("[SCHEDULER] Iniciando scheduler...")
        self._running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        print("[SCHEDULER] Hilo activo")

        while self._running:
            try:
                now = datetime.now()
                devices = self.device_repo.find_active()

                for device in devices:
                    try:
                        # lock por dispositivo → evita sync simultáneos
                        if device.device_id not in self._device_locks:
                            self._device_locks[device.device_id] = threading.Lock()

                        lock = self._device_locks[device.device_id]

                        # si ya se está sincronizando → saltar
                        if lock.locked():
                            continue

                        # nunca sincronizado
                        if device.last_sync_at is None:
                            print(f"[SCHEDULER] Sync inicial → {device.name}")
                            threading.Thread(
                                target=self._safe_sync,
                                args=(device.device_id, lock),
                                daemon=True
                            ).start()
                            continue

                        next_sync = device.last_sync_at + timedelta(
                            seconds=device.interval_seconds
                        )

                        if now >= next_sync:
                            print(f"[SCHEDULER] Sync programado → {device.name}")
                            threading.Thread(
                                target=self._safe_sync,
                                args=(device.device_id, lock),
                                daemon=True
                            ).start()

                    except Exception as e:
                        print(f"[SCHEDULER] ERROR en device {device.device_id}: {e}")

                time.sleep(10)

            except Exception as e:
                print(f"[SCHEDULER] ERROR GLOBAL: {e}")
                time.sleep(5)

    def _safe_sync(self, device_id, lock):
        with lock:
            try:
                print(f"[SYNC] Iniciando device {device_id}")
                self.sync_service.sync_device(device_id)
                print(f"[SYNC] Finalizado device {device_id}")
            except Exception as e:
                print(f"[SYNC] ERROR en device {device_id}: {e}")

    def stop(self):
        print("[SCHEDULER] Deteniendo scheduler...")
        self._running = False