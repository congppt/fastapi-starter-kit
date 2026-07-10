from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal, Protocol


@dataclass(frozen=True, slots=True)
class BlobMetadata:
    object_name: str
    size: int
    content_type: str | None = None
    etag: str | None = None
    last_modified: datetime | None = None


@dataclass(frozen=True, slots=True)
class BlobUploadUrl:
    url: str
    method: Literal["PUT", "POST"]
    fields: dict[str, str] | None = None
    expires_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class BlobDownloadUrl:
    url: str
    expires_at: datetime | None = None


class IBlobStorage(Protocol):
    """
    Blob storage contract for uploading, downloading, deleting, and getting the metadata of files.
    """

    async def upload(self, object_key: str, file: bytes) -> str:
        """Upload a file to the blob storage and return the object key."""

    async def download(self, object_key: str) -> bytes:
        """Download a file from the blob storage and return the bytes."""

    async def delete(self, object_key: str) -> bool:
        """Delete a file from the blob storage and return True if successful, False otherwise."""

    async def get_metadata(self, object_key: str) -> BlobMetadata:
        """Get the metadata of a file in the blob storage."""


class IBlobUrlGenerator(Protocol):
    async def create_upload_url(
        self, object_key: str, expires_in: timedelta | None = None
    ) -> BlobUploadUrl:
        """Generate upload URL for a file in the blob storage."""

    async def create_download_url(
        self, object_key: str, expires_in: timedelta | None = None
    ) -> BlobDownloadUrl:
        """Generate download URL for a file in the blob storage."""