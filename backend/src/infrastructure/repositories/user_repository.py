from abc import ABC, abstractmethod
from src.domain.models.user import User


class UserRepository(ABC):

    @abstractmethod
    def find_by_external_id(self, external_id: str) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass
