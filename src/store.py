from typing import List

from sqlalchemy.orm import Session

from .models import Link, Base
from .db import engine, SessionLocal  # assuming a db module provides engine & session factory


def get_db() -> Session:
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


def get_all_links_sorted() -> List[Link]:
    """
    Retrieve all Link objects ordered by click_count descending.
    This helper is used by the GET /api/links endpoint.
    """
    session = SessionLocal()
    try:
        links = (
            session.query(Link)
            .order_by(Link.click_count.desc())
            .all()
        )
        return links
    finally:
        session.close()