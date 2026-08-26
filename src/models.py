from datetime import datetime
from typing import Optional, Dict

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    def to_dict(self) -> Dict[str, Optional[object]]:
        """
        Convert the Link instance into a JSON‑serializable dictionary.
        Handles ``created_at`` being ``None`` gracefully.
        """
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "click_count": self.click_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }