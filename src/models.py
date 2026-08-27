from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Link:
    id: int
    original_url: str
    short_code: str
    click_count: int = 0
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Return a JSON‑serializable representation of the Link.
        ``created_at`` is converted to ISO‑8601 string if present,
        otherwise ``None`` is emitted.
        """
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "click_count": self.click_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }