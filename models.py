from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict

@dataclass
class Link:
    original_url: str
    short_code: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    click_count: int = 0

    def increment_click(self) -> None:
        """Increase the click count for this link."""
        self.click_count += 1

    def to_dict(self) -> Dict[str, object]:
        """
        Return a JSON‑serializable representation of the Link.
        datetime is converted to ISO‑8601 string.
        """
        return {
            "original_url": self.original_url,
            "short_code": self.short_code,
            "created_at": self.created_at.isoformat(),
            "click_count": self.click_count,
        }