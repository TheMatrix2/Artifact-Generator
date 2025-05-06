import os
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

from source.XMLAttribute import XMLAttribute
from source.XMLAggregation import XMLAggregation
from source.XMLClass import XMLClass

class ArtifactGenerator:
    """Класс для формирования итоговых файлов"""
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.classes: Dict[str, XMLClass] = {}
        self.aggregations: List[XMLAggregation] = []
        self.root_class: Optional[XMLClass] = None

    def process(self):
        """Парсинг исходного файла"""
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        for class_elem in root.findall("Class"):
            name = class_elem.get("name")
            is_root = class_elem.get("isRoot") == "true"
            documentation = class_elem.get("documentation", "")

            xml_class = XMLClass(name, documentation, is_root)

            for attr_elem in class_elem.findall("Attribute"):
                attr_name = attr_elem.get("name")
                attr_type = attr_elem.get("type")
                xml_class.add_attribute(XMLAttribute(attr_name, attr_type))

            self.classes[name] = xml_class

            if is_root:
                self.root_class = xml_class

        for agg_elem in root.findall("Aggregation"):
            source = agg_elem.get("source")
            target = agg_elem.get("target")
            source_multiplicity = agg_elem.get("sourceMultiplicity")
            target_multiplicity = agg_elem.get("targetMultiplicity")

            aggregation = XMLAggregation(source, target, source_multiplicity, target_multiplicity)
            self.aggregations.append(aggregation)

            source_class = self.classes[source]
            source_class.min_count = aggregation.min_count
            source_class.max_count = aggregation.max_count

            target_class = self.classes[target]
            target_class.add_aggregation(source_class)

    def generate_config(self, output_path: str) -> None:
        if not self.root_class:
            raise ValueError("No root class found in model")

        with open(output_path, "w") as f:
            f.write(self._generate_class_xml(self.root_class, 0))

    def _generate_class_xml(self, xml_class: XMLClass, indent_level: int) -> str:
        indent = "    " * indent_level
        result = f"{indent}<{xml_class.name}>\n"

        for attr in xml_class.attributes:
            result += f"{indent}    <{attr.name}>{attr.type}</{attr.name}>\n"

        for agg in xml_class.aggregations:
            result += self._generate_class_xml(agg, indent_level + 1)

        result += f"{indent}</{xml_class.name}>\n"
        return result

    def generate_meta(self, output_path: str) -> None:
        result = []

        for cls in sorted(self.classes.values(), key=lambda c: len(c.aggregations)):
            result.append(cls.to_dict())

        with open(output_path, "w") as f:
            json.dump(result, f, indent=4)

def main():
    processor = ArtifactGenerator("test_input.xml")
    processor.process()
    if not os.path.exists('out/'):
        os.mkdir('out')

    try:
        processor.generate_config(os.path.join('out', 'config.xml'))
    except Exception as e:
        print(f'Failed to generate config.xml: {e}')
    else:
        print('Successfully generated config.xml')

    try:
        processor.generate_meta(os.path.join('out', 'meta.json'))
    except Exception as e:
        print(f'Failed to generate meta.json: {e}')
    else:
        print('Successfully generated meta.json')


if __name__ == "__main__":
    main()