from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Link:
    """
    Represents a shortened link with metadata.
    """
    id: int
    short_code: str
    original_url: str
    click_count: int = 0
    created_at: Optional[datetime] = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        """
        Convert the Link instance to a JSON‑serialisable dictionary.
        Handles ``created_at`` being ``None`` safely.
        """
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "click_count": self.click_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }