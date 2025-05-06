from typing import Dict, List, Any

from source.XMLElement import XMLElement
from source.XMLAttribute import XMLAttribute


class XMLClass(XMLElement):
    """Представление модели XML"""
    def __init__(self, name: str, documentation: str = '', is_root: bool = False):
        super().__init__(name, documentation, is_root)
        self.attributes: List[XMLAttribute] = []
        self.aggregations: List[XMLClass] = []
        self.min_count: str = '1'
        self.max_count: str = '1'

    def add_aggregation(self, xml_class: 'XMLClass') -> None:
        self.aggregations.append(xml_class)

    def add_attribute(self, attribute: XMLAttribute) -> None:
        self.attributes.append(attribute)

    def to_dict(self) -> Dict[str, Any]:
        result = {
            'class': self.name,
            'documentation': self.documentation,
            'isRoot': self.is_root,
            'parameters': []
        }

        if not self.is_root:
            result['min'] = self.min_count
            result['max'] = self.max_count

        for aggregation in self.aggregations:
            result['parameters'].append({
                'name': aggregation.name,
                'type': 'class'
            })

        for attr in self.attributes:
            result["parameters"].append(attr.to_dict())

        return result
