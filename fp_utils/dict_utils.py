import re
from typing import Dict, Any, Optional


class DictUtil:

    @classmethod
    def find_value_by_regex(cls, data: Dict[str, Any], regex: str) -> Any:
        """Search for a value matching the regex in a nested dictionary or list structure."""
        pattern = re.compile(regex)
        return cls._search(data, pattern, return_dict=False)

    @classmethod
    def find_dict_by_value_regex(cls, data: Dict[str, Any], regex: str) -> Optional[Dict[str, Any]]:
        """Search for a value matching the regex and return the containing dictionary."""
        pattern = re.compile(regex)
        return cls._search(data, pattern, return_dict=True)

    @classmethod
    def _search(cls, value: Any, pattern: re.Pattern, return_dict: bool) -> Optional[Dict[str, Any]]:
        """Recursively search for a matching value in dictionaries and lists, optionally returning the containing dictionary."""
        if isinstance(value, dict):
            for key, val in value.items():
                if isinstance(val, str) and pattern.search(val):
                    return value if return_dict else val
                result = cls._search(val, pattern, return_dict)
                if result:
                    return result
        elif isinstance(value, list):
            for item in value:
                result = cls._search(item, pattern, return_dict)
                if result:
                    return result
        return None
    
    @classmethod
    def find_by_key(cls, data: Dict[str, Any], target_key: str) -> Optional[Dict[str, Any]]:
        """Search for a specific key in a nested dictionary or list and return the containing dictionary."""
        return cls._search_key(data, target_key)

    @classmethod
    def _search_key(cls, value: Any, target_key: str) -> Optional[Dict[str, Any]]:
        """Recursively search for a specific key in dictionaries and lists."""
        if isinstance(value, dict):
            if target_key in value:
                return value  # Return the dictionary that contains the target key
            for val in value.values():
                result = cls._search_key(val, target_key)
                if result:
                    return result
        elif isinstance(value, list):
            for item in value:
                result = cls._search_key(item, target_key)
                if result:
                    return result
        return None