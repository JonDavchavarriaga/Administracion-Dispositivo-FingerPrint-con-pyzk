from src.domain.models.user import User


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    # ========= Sync desde dispositivo =========
    def find_or_create_from_device(self, external_id: str, name: str) -> User:
        user = self.user_repository.find_by_external_id(external_id)

        if user:
            return user

        shadow_user = User(
            user_id=None,
            external_id=external_id,
            name=name,
            cost_center_id=None,   # ← viene vacío
            is_active=True
        )
        return self.user_repository.save(shadow_user)

    # ========= CRUD =========
    def list_users(self):
        return self.user_repository.find_all()

    def update_user(self, user_id: int, name: str, is_active: bool):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.name = name
        user.is_active = is_active
        return self.user_repository.update(user)

    def assign_cost_center(self, user_id: int, cost_center_id: int | None):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        user.cost_center_id = cost_center_id
        return self.user_repository.update(user)
