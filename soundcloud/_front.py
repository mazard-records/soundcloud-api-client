import re
from functools import lru_cache

from httpx import AsyncClient

from ._asynctool import aiter

DEFAULT_FRONT_URL = "https://soundcloud.com"
PATTERN_SRCS = re.compile(r"<script crossorigin src=\"([^\"]+)\">")
PATTERN_HYDRATE = re.compile(r"")
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
    async for url in aiter(urls):
        script = await client.get(url)
        script.raise_for_status()
        match = PATTERN_VARIABLE.search(script.text)
        if match:
            return match.group(1)


def _get_normalized_url(url: str) -> str:
    if url.startswith(DEFAULT_FRONT_URL):
        url = url[len(DEFAULT_FRONT_URL) :]
    if not url.startswith("/"):
        url = f"/{url}"
    if "?" in url:
        url = url.split("?").pop(0)
    return url


@lru_cache(maxsize=20)
async def get_track_id_from_url(track_url: str) -> int:
    client = SoundcloudFrontClient()
    track_url = _get_normalized_url(track_url)
    track = await client(track_url)
    track.raise_for_status()
    match = PATTERN_HYDRATE.search(track.text)
    if match:
        hydration = match.group(1)
        # TODO: lookup for sound object.
