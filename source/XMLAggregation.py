from typing import Tuple


class XMLAggregation:
    """Класс отношений между классами XML"""
    def __init__(self, source: str, target: str, source_multiplicity: str, target_multiplicity: str):
        self.source = source
        self.target = target
        self.source_multiplicity = source_multiplicity
        self.target_multiplicity = target_multiplicity
        self.min_count, self.max_count = self._parse_multiplicity(source_multiplicity)

    @staticmethod
    def _parse_multiplicity(multiplicity: str) -> Tuple[str, str]:
        if '..' in multiplicity:
            min_value, max_value = multiplicity.split('..')
            return min_value, max_value
        else:
            return multiplicity, multiplicity
