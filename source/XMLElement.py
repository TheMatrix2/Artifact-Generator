from typing import Dict, Any


class XMLElement:
    """Класс простого элемента XML файла"""
    def __init__(self, name: str, documentation: str = '', is_root: bool = False):
        self.name = name
        self.documentation = documentation
        self.is_root = is_root

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь для подготовки данных"""
        raise NotImplementedError("Must be implemented by subclasses")
