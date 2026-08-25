from dataclasses import dataclass

@dataclass
class Url:
    """
    Simple data model representing a URL mapping.
    """
    original_url: str
    short_code: str