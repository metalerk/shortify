from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from sqlalchemy.orm import Session
from app.core.config import get_db
from app.data.repository import UrlRepository
from app.domain.models import Url, UrlUpdate


REQUESTS = Counter('http_requests_total', 'Total number of HTTP requests')
IN_PROGRESS = Gauge('http_in_progress', 'Number of HTTP requests in progress')
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'Histogram of HTTP request durations in seconds')

router = APIRouter()

@router.get("/")
def read_root():
    REQUESTS.inc()  # increment counter
    IN_PROGRESS.set(1)  # 1 request is in progress

    with REQUEST_DURATION.time():  # measure time of request
        return {"message": "ok"}

# custom metrics
@router.get("/custom_metrics", response_class=PlainTextResponse)
def custom_metrics():
    return generate_latest()


@router.post("/shorten", status_code=status.HTTP_201_CREATED)
def shorten_url(request: Url, db: Session = Depends(get_db)):
    """
    Shortens a URL by generating a shortcode or using a provided one.

    :param request: The input request containing `url` and optional `shortcode`.
    :param db: Database session dependency.
    :return: JSON response with `shortcode` and `update_id`.
    """
    if not request.shortcode:
        request.generate_shortcode()

    repository = UrlRepository(db)
    try:
        saved_url = repository.save(request)
    except HTTPException as e:
        if e.status_code == status.HTTP_409_CONFLICT:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Shortcode already in use"
            )
        raise

    return {"shortcode": saved_url.shortcode, "update_id": saved_url.update_id}


@router.post("/update/{update_id}", status_code=status.HTTP_201_CREATED)
def update_url(update_id: str, request: UrlUpdate, db: Session = Depends(get_db)):
    """
    Updates the URL associated with a given update ID.

    :param update_id: The unique identifier for the update operation.
    :param request: The input request containing the new `url`.
    :param db: Database session dependency.
    :return: JSON response with `shortcode` of the updated URL.
    """
    repository = UrlRepository(db)
    updated_url = repository.update_url(update_id, str(request.url))
    return {"shortcode": updated_url.shortcode}


@router.get("/{shortcode}", status_code=status.HTTP_302_FOUND)
def redirect(shortcode: str, db: Session = Depends(get_db)):
    """
    Redirects to the URL associated with the given shortcode.

    :param shortcode: The shortcode to resolve.
    :param db: Database session dependency.
    :return: RedirectResponse to the resolved URL.
    """
    repository = UrlRepository(db)
    url_obj = repository.find_by_shortcode(shortcode)
    if not url_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shortcode not found"
        )

    url_obj.last_redirect = datetime.utcnow()
    url_obj.redirect_count += 1
    db.commit()

    return RedirectResponse(url=url_obj.url, status_code=status.HTTP_302_FOUND)


@router.get("/{shortcode}/stats", status_code=status.HTTP_200_OK)
def get_stats(shortcode: str, db: Session = Depends(get_db)):
    """
    Retrieves statistics for a given shortcode.

    :param shortcode: The shortcode to retrieve statistics for.
    :param db: Database session dependency.
    :return: JSON response with `created`, `lastRedirect`, `redirectCount`, and `shortcode`.
    """
    repository = UrlRepository(db)
    url_obj = repository.find_by_shortcode(shortcode)
    if not url_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shortcode not found"
        )

    return {
        "shortcode": url_obj.shortcode,
        "created": url_obj.created.isoformat() if url_obj.created else None,
        "lastRedirect": (
            url_obj.last_redirect.isoformat() if url_obj.last_redirect else None
        ),
        "redirectCount": url_obj.redirect_count,
    }
