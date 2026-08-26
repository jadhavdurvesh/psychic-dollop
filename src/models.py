from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import datetime

Base = declarative_base()

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    original_url = Column(String, nullable=False)
    short_url = Column(String, nullable=False, unique=True)
    click_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        """Return a JSON‑serializable representation of the Link."""
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_url": self.short_url,
            "click_count": self.click_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }