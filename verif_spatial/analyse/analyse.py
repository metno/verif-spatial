
class Analyse:
    """Analyse base class"""
    def __init__(
        self,
        field_2d,
    ) -> None:
        self.field_2d = field_2d.astype(float)
