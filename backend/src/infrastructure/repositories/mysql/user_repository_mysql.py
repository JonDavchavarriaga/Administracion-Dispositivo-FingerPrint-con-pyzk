from sqlalchemy.orm import Session
from src.domain.models.user import User
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import UserEntity


class UserRepositoryMySQL(UserRepository):

    def __init__(self):
        self.session_factory = SessionLocal

    def find_by_external_id(self, external_id: str) -> User | None:
        session: Session = self.session_factory()
        try:
            entity = (
                session.query(UserEntity)
                .filter(UserEntity.external_id == external_id)
                .first()
            )
            if not entity:
                return None

            return User(
                user_id=entity.id,
                external_id=entity.external_id,
                name=entity.name,
                active=entity.active
            )
        finally:
            session.close()

    def save(self, user: User) -> User:
        session: Session = self.session_factory()
        try:
            entity = UserEntity(
                external_id=user.external_id,
                name=user.name,
                active=user.active
            )
            session.add(entity)
            session.commit()
            session.refresh(entity)

            return User(
                user_id=entity.id,
                external_id=entity.external_id,
                name=entity.name,
                active=entity.active
            )
        finally:
            session.close()
