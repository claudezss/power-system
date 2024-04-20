class Base:
    name: str

    unit_mapping: dict[str, str]

    def __repr__(self) -> str:
        return str(self.name)
