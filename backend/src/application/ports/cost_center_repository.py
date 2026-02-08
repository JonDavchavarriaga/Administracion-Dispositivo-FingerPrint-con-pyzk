from abc import ABC, abstractmethod
from src.domain.models.costCenter import CostCenter

class CostCenterRepository(ABC):

    @abstractmethod
    def save(self, cost_center: CostCenter) -> CostCenter:
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, cost_center_id: int) -> CostCenter | None:
        pass

    @abstractmethod
    def update(self, cost_center: CostCenter) -> CostCenter:
        pass

    @abstractmethod
    def delete(self, cost_center_id: int):
        pass

