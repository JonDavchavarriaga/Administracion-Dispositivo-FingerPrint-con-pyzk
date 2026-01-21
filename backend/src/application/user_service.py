from src.domain.models.user import User


class UserService:

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def find_or_create_from_device(self, external_id: str, name: str) -> User:
        """
        Garantiza que el usuario exista localmente (BD)
        """
        user = self.user_repository.find_by_external_id(external_id)

        if user:
            return user

        # Materialización local
        shadow_user = User(
            user_id=None,
            external_id=external_id,
            name=name,
            active=True
        )
        return self.user_repository.save(shadow_user)

    def find_by_external_id(self, external_id: str) -> User | None:
        return self.user_repository.find_by_external_id(external_id)
