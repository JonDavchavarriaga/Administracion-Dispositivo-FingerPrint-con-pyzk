class User:
    def __init__(
        self,
        user_id,
        external_id,
        name,
        is_active=True,
        cost_center_id=None

    ):
        self.user_id = user_id          # ID interno DB
        self.external_id = external_id  # ID del huellero
        self.name = name
        self.is_active = is_active,
        self.cost_center_id = cost_center_id
