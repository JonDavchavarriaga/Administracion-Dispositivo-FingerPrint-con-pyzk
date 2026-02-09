from src.domain.models.costCenter import CostCenter


class CostCenterService:
    def __init__(self, repository):
        self.repository = repository

    def register_cost_center(self,name: str) -> CostCenter:
        cost_center = CostCenter(name=name)
        return self.repository.save(cost_center)

    def list_cost_centers(self):
        return self.repository.find_all()

    def update_cost_center(self, cost_center_id: int, name: str):
        cc = self.repository.find_by_id(cost_center_id)
        if not cc:
            raise ValueError("Cost center not found")

        cc.name = name
        return self.repository.update(cc)

    def delete_cost_center(self, cost_center_id: int):
        self.repository.delete(cost_center_id)
