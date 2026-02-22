import datetime
import logging

import google.auth
import google.auth.transport.requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from google.cloud import storage
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/videos", tags=["video-serve"])


def _generate_signed_url(bucket_name: str, blob_name: str, expiry_minutes: int = 60) -> str:
    """
    Generate a GCS Signed URL v4 using Application Default Credentials (ADC).
    Works on Cloud Run without a service account key file — the attached
    service account is used automatically.
    Requires: roles/storage.objectViewer on the bucket
              roles/iam.serviceAccountTokenCreator on the service account (self)
    """
    credentials, _ = google.auth.default()

    # Refresh so we have a valid access token for the signing request
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)

    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    signed_url = blob.generate_signed_url(
        expiration=datetime.timedelta(minutes=expiry_minutes),
        method="GET",
        version="v4",
        # ADC-based signing — no key file required on Cloud Run
        service_account_email=credentials.service_account_email,
        access_token=credentials.token,
    )
    return signed_url


@router.get("/serve/{filename}")
async def serve_video(filename: str):
    """
    Serve a video file:
    - Local dev: streams directly from ASSETS_PATH if the file exists (fast, no GCS call).
    - Cloud Run: generates a short-lived GCS Signed URL and redirects the browser to it.
      The browser then streams directly from GCS with full byte-range/seeking support.
    """
    # ── Local file check ──────────────────────────────────────────────────────
    local_path = Path(settings.ASSETS_PATH) / filename
    if local_path.exists() and local_path.is_file():
        logger.info(f"Serving local file: {local_path}")
        return FileResponse(
            path=str(local_path),
            media_type="video/mp4",
            filename=filename,
        )

    # ── GCS Signed URL fallback ───────────────────────────────────────────────
    blob_name = f"{settings.GCS_BLOB_PREFIX.strip('/')}/{filename}"
    logger.info(f"Local file not found. Generating signed URL for gs://{settings.GCS_BUCKET}/{blob_name}")

    try:
        signed_url = _generate_signed_url(
            bucket_name=settings.GCS_BUCKET,
            blob_name=blob_name,
        )
    except Exception as e:
        logger.error(f"Failed to generate signed URL: {e}")
        raise HTTPException(status_code=500, detail=f"Could not generate video URL: {e}")

    # 302 redirect — browser fetches video directly from GCS (byte-range works natively)
    return RedirectResponse(url=signed_url, status_code=302)

