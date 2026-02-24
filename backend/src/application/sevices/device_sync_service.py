from src.infrastructure.devices.zk_device import ZKFingerprintDevice


class DeviceSyncService:

    def __init__(self, device_repo, attendance_service, user_service, user_device_repo):
        self.device_repo = device_repo
        self.attendance_service = attendance_service
        self.user_service = user_service
        self.user_device_repo = user_device_repo

    def sync_device(self, device_id: int):
        device = self.device_repo.find_by_id(device_id)
        if not device or not device.is_active:
            print(f"[SYNC] Dispositivo {device_id} no encontrado o inactivo")
            return

        print("=" * 60)
        print(f"[SYNC] Iniciando sincronización dispositivo {device.device_id}")
        print(f"[SYNC] IP: {device.ip}:{device.port}")

        zk_device = ZKFingerprintDevice(
            ip=device.ip,
            port=device.port
        )

        try:
            zk_device.connect()
            print("[SYNC] Conectado al dispositivo")

            # ===== Usuarios =====
            print("[SYNC] Obteniendo usuarios del dispositivo...")
            users = zk_device.get_users()
            print(f"[SYNC] Usuarios encontrados: {len(users)}")

            user_map = {}
            created_links = 0

            for u in users:
                user = self.user_service.find_or_create_from_device(
                    external_id=str(u["user_id"]),
                    name=u["name"]
                )

                self.user_device_repo.link_user_to_device(
                    user_id=user.user_id,
                    device_id=device.device_id
                )

                created_links += 1
                user_map[str(u["user_id"])] = user

            print(f"[SYNC] Relaciones user-device procesadas: {created_links}")

            # ===== Marcaciones =====
            print("[SYNC] Buscando última marcación guardada...")
            last_timestamp = self.attendance_service.get_last_timestamp(device.device_id)

            if last_timestamp:
                print(f"[SYNC] Última marcación en BD: {last_timestamp}")
            else:
                print("[SYNC] No hay marcaciones previas → sync completo")

            print("[SYNC] Obteniendo marcaciones del dispositivo...")
            records = zk_device.get_attendance()
            print(f"[SYNC] Marcaciones obtenidas del dispositivo: {len(records)}")

            processed = 0
            skipped = 0

            for r in records:
                ts = r["timestamp"]

                if last_timestamp and ts <= last_timestamp:
                    skipped += 1
                    continue

                user = user_map.get(str(r["user_id"]))
                if not user:
                    skipped += 1
                    continue

                self.attendance_service.process_record(
                    user_id=user.user_id,
                    device_id=device.device_id,
                    timestamp=ts
                )

                processed += 1

            print(f"[SYNC] Marcaciones nuevas guardadas: {processed}")
            print(f"[SYNC] Marcaciones ignoradas: {skipped}")

            # actualizar last_sync_at
            self.device_repo.update_last_sync(device.device_id)
            print("[SYNC] last_sync_at actualizado")

            print(f"[SYNC] ✔ Finalizado dispositivo {device.device_id}")

        except Exception as e:
            print(f"[SYNC][ERROR] Dispositivo {device.device_id}: {e}")

        finally:
            zk_device.disconnect()
            print("[SYNC] Desconectado del dispositivo")

    def sync_all(self):
        print("\n[SYNC] ===== SINCRONIZACIÓN GLOBAL =====")
        devices = self.device_repo.find_active()
        print(f"[SYNC] Dispositivos activos: {len(devices)}")

        for d in devices:
            self.sync_device(d.device_id)

        print("[SYNC] ===== FIN SINCRONIZACIÓN GLOBAL =====\n")
