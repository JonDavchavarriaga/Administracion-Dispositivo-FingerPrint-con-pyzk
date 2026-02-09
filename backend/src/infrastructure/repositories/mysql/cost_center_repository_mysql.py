from src.application.ports.cost_center_repository import CostCenterRepository
from src.infrastructure.repositories.mysql.database import SessionLocal
from src.infrastructure.repositories.mysql.models import CostCenterTable
from src.domain.models.costCenter import CostCenter

class CostCenterRepositoryMySQL(CostCenterRepository):

    def save(self, cost_center: CostCenter) -> CostCenter:
        db = SessionLocal()
        try:
            model = CostCenterTable(
                name=cost_center.name
            )
            db.add(model)
            db.commit()
            db.refresh(model)

            cost_center.id = model.id
            return cost_center
        finally:
            db.close()

    def find_all(self):
        db = SessionLocal()
        try:
            rows = db.query(CostCenterTable).all()
            return [self._to_domain(r) for r in rows]
        finally:
            db.close()

    def find_by_id(self, id: int) -> CostCenter | None:
        db = SessionLocal()
        try:
            row = (
                db.query(CostCenterTable)
                .filter(CostCenterTable.id == id)
                .first()
            )
            return self._to_domain(row) if row else None
        finally:
            db.close()

    def update(self, cost_center: CostCenter) -> CostCenter:
        db = SessionLocal()
        try:
            row = (
                db.query(CostCenterTable)
                .filter(CostCenterTable.id == cost_center.id)
                .first()
            )

            if not row:
                raise ValueError("Cost center not found")

            row.name = cost_center.name
            db.commit()
            return cost_center
        finally:
            db.close()

    def delete(self, id: int):
        db = SessionLocal()
        try:
            row = (
                db.query(CostCenterTable)
                .filter(CostCenterTable.id == id)
                .first()
            )

            if row:
                db.delete(row)
                db.commit()
        finally:
            db.close()

    def _to_domain(self, row: CostCenterTable) -> CostCenter:
        return CostCenter(
            id=row.id,
            name=row.name
        )
