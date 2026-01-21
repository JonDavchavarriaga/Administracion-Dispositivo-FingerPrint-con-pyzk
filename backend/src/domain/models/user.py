class User:
    def __init__(
        self,
        user_id,
        external_id,
        name,
        active=True
    ):
        self.user_id = user_id          # ID interno DB
        self.external_id = external_id  # ID del huellero
        self.name = name
        self.active = active
