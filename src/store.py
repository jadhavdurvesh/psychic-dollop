from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from src.models import Base, Link

# Use an SQLite file database; tests can override this via the ENGINE env var if needed.
engine = create_engine("sqlite:///links.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker(bind=engine))


def get_all_links_sorted():
    """
    Retrieve all Link records ordered by click_count descending.
    Returns a list of Link objects.
    """
    session = Session()
    try:
        links = (
            session.query(Link)
            .order_by(desc(Link.click_count))
            .all()
        )
        return links
    finally:
        session.close()