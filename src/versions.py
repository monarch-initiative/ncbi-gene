"""Upstream source version fetcher for ncbi-gene."""

from __future__ import annotations

import datetime
import email.utils
from pathlib import Path
from typing import Any

import requests

from kozahub_metadata_schema.writer import urls_from_download_yaml


INGEST_DIR = Path(__file__).resolve().parents[1]
DOWNLOAD_YAML = INGEST_DIR / "download.yaml"


def _now_iso() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _ncbi_version_from_url(url: str) -> tuple[str, str]:
    """NCBI Gene's gene_info.gz has no in-band version. Use HTTP Last-Modified."""
    try:
        r = requests.head(url, allow_redirects=True, timeout=10)
        r.raise_for_status()
        lm = r.headers.get("Last-Modified")
        if not lm:
            return "unknown", "unavailable"
        dt = email.utils.parsedate_to_datetime(lm)
        return dt.date().isoformat(), "http_last_modified"
    except Exception:
        return "unknown", "unavailable"


def get_source_versions() -> list[dict[str, Any]]:
    urls = urls_from_download_yaml(DOWNLOAD_YAML)
    # gene_info.gz is the canonical version-bearing file
    primary = next((u for u in urls if u.endswith("gene_info.gz")), urls[0] if urls else "")
    ver, method = _ncbi_version_from_url(primary) if primary else ("unknown", "unavailable")
    return [
        {
            "id": "infores:ncbi-gene",
            "name": "NCBI Gene",
            "urls": urls,
            "version": ver,
            "version_method": method,
            "retrieved_at": _now_iso(),
        }
    ]
