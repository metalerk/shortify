from sqlalchemy import Column, String, Integer, DateTime
from app.data.database import Base
from datetime import datetime


class UrlModel(Base):
    """
    SQLAlchemy model for the URLs table.
    """

    __tablename__ = "urls"
    shortcode = Column(String, primary_key=True, index=True)
    url = Column(String, nullable=False)
    update_id = Column(String, unique=True, nullable=False)
    created = Column(DateTime, default=datetime.utcnow)
    last_redirect = Column(DateTime, nullable=True)
    redirect_count = Column(Integer, default=0)
