from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Link:
    id: int
    original_url: str
    short_code: str
    click_count: int = 0
    created_at: datetime = datetime.utcnow()

    def to_dict(self) -> dict:
        """
        Return a JSON‑serialisable dictionary representation of the Link.
        The datetime is converted to an ISO‑8601 string.
        """
        data = asdict(self)
        # datetime objects are not JSON serialisable by default
        if isinstance(data.get('created_at'), datetime):
            data['created_at'] = data['created_at'].isoformat()
        return data