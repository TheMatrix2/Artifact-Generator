from typing import Dict


class XMLAttribute:
    """Класс для хранения данных об атрибутах классов XML"""
    def __init__(self, name: str, attr_type: str):
        self.name = name
        self.type = attr_type

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "type": self.type
        }
