import asyncio
from typing import Any, Optional, Union
from urllib.parse import urlencode

from httpx import Client

from ._front import get_client_id, get_track_id_from_url
from ._models import SoundcloudTrack

DEFAULT_API_URL = "https://api-v2.soundcloud.com"


class SoundcloudClient(object):
    """ """

    def __init__(
        self,
        client_id: Optional[str] = None,
        url: str = DEFAULT_API_URL,
    ) -> None:
        if client_id is None:
            client_id = asyncio.run(get_client_id())
        self._client_id = client_id
        self._transport = Client(base_url=url)

    def _url(self, path: str, **args: dict[str, Any]) -> str:
        return f"{path}?{urlencode(args.update(client_id=self._client_id))}"

    def track(self, track_id_or_url: Union[int, str]) -> SoundcloudTrack:
        """ """
        track_id = asyncio.run(get_track_id_from_url(track_id_or_url))
        url = self._url(f"/tracks/{track_id}")
        response = self._transport.get(url)
        response.raise_for_status()
        return SoundcloudTrack(_client=self, **response.json())

    def comments(self, track_id: int) -> ...:
        """ """
        url = self._url(
            f"/tracks/{track_id}/comments",
            limit=20,
            linked_partitioning=1,
            offset=0,
        )
        response = self._transport.get(url)
        response.raise_for_status()
        return ...
