from abc import ABC, abstractmethod
from src.domain.models.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_external_id(self, external_id: str) -> User | None:
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def update_cost_center(self, user_id: int, cost_center_id: int | None):
        pass
