from sqlalchemy.orm import Session
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException, status
from app.data.models import UrlModel
from app.domain.models import Url


class UrlRepository:
    """
    Repository for managing URL entities in the database.
    """

    def __init__(self, db: Session):
        """
        Initializes the repository with a database session.

        :param db: SQLAlchemy session object.
        """
        self.db = db

    def save(self, url_obj: Url) -> UrlModel:
        """
        Save a new URL entity to the database.

        :param url_obj: Pydantic model containing URL data.
        :return: The saved SQLAlchemy URL entity.
        """
        existing = (
            self.db.query(UrlModel).filter_by(shortcode=url_obj.shortcode).first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Shortcode already in use"
            )

        if not url_obj.update_id:
            url_obj.update_id = str(uuid4())

        db_url = UrlModel(
            shortcode=url_obj.shortcode,
            url=str(url_obj.url),
            update_id=url_obj.update_id,
            created=url_obj.created or datetime.utcnow(),
            last_redirect=url_obj.last_redirect,
            redirect_count=url_obj.redirect_count,
        )

        self.db.add(db_url)
        self.db.commit()
        self.db.refresh(db_url)
        return db_url

    def find_by_shortcode(self, shortcode: str) -> UrlModel:
        """
        Find a URL entity by its shortcode.

        :param shortcode: The shortcode to search for.
        :return: The URL entity, if found.
        """
        db_url = self.db.query(UrlModel).filter_by(shortcode=shortcode).first()
        if not db_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shortcode not found"
            )
        return db_url

    def update_url(self, update_id: str, new_url: str) -> UrlModel:
        """
        Update the URL for a given update ID.

        :param update_id: The unique update ID.
        :param new_url: The new URL to set.
        :return: The updated URL entity.
        """
        db_url = self.db.query(UrlModel).filter_by(update_id=update_id).first()
        if not db_url:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The provided update ID does not exist",
            )

        db_url.url = new_url
        self.db.commit()
        self.db.refresh(db_url)
        return db_url

    def increment_redirect_count(self, shortcode: str) -> UrlModel:
        """
        Increment the redirect count for a given shortcode.

        :param shortcode: The shortcode whose redirect count should be incremented.
        :return: The updated URL entity.
        """
        db_url = self.find_by_shortcode(shortcode)
        db_url.last_redirect = datetime.utcnow()
        db_url.redirect_count += 1
        self.db.commit()
        self.db.refresh(db_url)
        return db_url
