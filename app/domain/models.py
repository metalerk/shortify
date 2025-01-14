from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class Url(BaseModel):
    """
    Pydantic model for URL entity.
    """

    url: HttpUrl
    shortcode: Optional[str] = None
    update_id: Optional[str] = None
    created: Optional[datetime] = datetime.utcnow()
    last_redirect: Optional[datetime] = None
    redirect_count: int = 0

    def generate_shortcode(self):
        """
        Generates a random shortcode for the URL.
        """
        import random, string

        self.shortcode = "".join(
            random.choices(string.ascii_letters + string.digits + "_", k=6)
        )


class UrlUpdate(BaseModel):
    """
    Pydantic model for updating a URL.
    """

    url: HttpUrl
