import re
from functools import lru_cache
from typing import Optional

from httpx import AsyncClient

from ._asynctool import aiter
from ._models import SoundcloudTrack

DEFAULT_FRONT_URL = "https://soundcloud.com"
PATTERN_SRCS = re.compile(r"<script crossorigin src=\"([^\"]+)\">")
PATTERN_HYDRATE = re.compile(r"window.__sc_hydration = (\[\{.+\}\]);")
PATTERN_VARIABLE = re.compile(r"\"client_id=([^\"]+)\"")


@lru_cache(maxsize=10)
def SoundcloudFrontClient(url: str = DEFAULT_FRONT_URL) -> AsyncClient:
    return AsyncClient(base_url=url)


@lru_cache(maxsize=1)
async def get_client_id() -> str:
    client = SoundcloudFrontClient()
    discover = await client.get("/discover")
    discover.raise_for_status()
    srcs = PATTERN_SRCS.finditer(discover.text)
    urls = [src.group(1) for src in srcs]
    client_id: Optional[str] = None
    async for url in aiter(urls):
        script = await client.get(url)
        script.raise_for_status()
        match = PATTERN_VARIABLE.search(script.text)
        if match:
            client_id = match.group(1)
    if client_id is None:
        # TODO: throw error
        pass
    return client_id


def _get_normalized_url(url: str) -> str:
    if url.startswith(DEFAULT_FRONT_URL):
        url = url[len(DEFAULT_FRONT_URL):]
    if not url.startswith("/"):
        url = f"/{url}"
    if "?" in url:
        url = url.split("?").pop(0)
    return url


@lru_cache(maxsize=20)
async def get_track_from_url(track_url: str) -> SoundcloudTrack:
    client = SoundcloudFrontClient()
    track_url = _get_normalized_url(track_url)
    track = await client.get(track_url)
    track.raise_for_status()
    match = PATTERN_HYDRATE.search(track.text)
    if not match:
        # TODO: throw error
        pass
    return SoundcloudTrack.from_raw_hydration(match.group(1))


@lru_cache(maxsize=20)
async def get_track_id_from_url(track_url: str) -> SoundcloudTrack:
    track = await get_track_from_url(track_url)
    return track.id
