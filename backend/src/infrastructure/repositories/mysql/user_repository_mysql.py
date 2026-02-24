from src.application.ports.user_repository import UserRepository
from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import UserTable
from src.domain.models.user import User


class UserRepositoryMySQL(UserRepository):

    def save(self, user: User) -> User:
        db = SessionLocal()
        try:
            model = UserTable(
                external_id=user.external_id,
                name=user.name,
                is_active=user.is_active,
                cost_center=user.cost_center_id
            )
            db.add(model)
            db.commit()
            db.refresh(model)

            user.user_id = model.id
            return user
        finally:
            db.close()

    def find_by_external_id(self, external_id: str):
        db = SessionLocal()
        try:
            u = db.query(UserTable).filter_by(external_id=external_id).first()
            return self._to_domain(u) if u else None
        finally:
            db.close()

    def find_all(self):
        db = SessionLocal()
        try:
            return [self._to_domain(u) for u in db.query(UserTable).all()]
        finally:
            db.close()

    def find_by_id(self, user_id: int):
        db = SessionLocal()
        try:
            u = db.query(UserTable).get(user_id)
            return self._to_domain(u) if u else None
        finally:
            db.close()

    def update_cost_center(self, user_id: int, cost_center_id: int | None):
        db = SessionLocal()
        try:
            u = db.query(UserTable).get(user_id)
            if u:
                u.cost_center_id = cost_center_id
                db.commit()
        finally:
            db.close()

    def _to_domain(self, u: UserTable) -> User:
        return User(
            user_id=u.id,
            external_id=u.external_id,
            name=u.name,
            is_active=u.is_active,
            cost_center_id=u.cost_center_id
        )
