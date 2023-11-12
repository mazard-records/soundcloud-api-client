import json
from typing import Any, Optional, TypeVar

from pydantic import AnyHttpUrl, BaseModel

from ._protocols import (
    SoundcloudClientProtocol,
    SoundcloudCommentsProtocol,
    SoundcloudTrackProtocol,
)

M = TypeVar("M")


class SoundcloudHydrationItem(BaseModel):
    hydratable: str
    data: Any


class BaseSoundcloudModel(BaseModel):
    """Base model with id and uri attributes."""

    _client: Optional[SoundcloudClientProtocol] = None
    id: int
    uri: AnyHttpUrl


class SoundcloudPaginableModel(BaseModel):
    """Base container for paginable collection."""

    collection: list[M]
    next_href: AnyHttpUrl


class SoundcloudComment(BaseSoundcloudModel):
    """@see:
    https://developers.soundcloud.com/docs/api/explorer/open-api#model-Comment
    """

    body: str
    timestamp: str

    track_id: int
    user_id: int


class SoundcloudComments(SoundcloudPaginableModel, SoundcloudCommentsProtocol):
    """@see:
    https://developers.soundcloud.com/docs/api/explorer/open-api#model-Comments
    """

    collection: list[SoundcloudComment]


class SoundcloudTrack(BaseSoundcloudModel, SoundcloudTrackProtocol):
    """@see:
    https://developers.soundcloud.com/docs/api/explorer/open-api#model-Track
    """

    title: str
    artwork_url: AnyHttpUrl
    duration: int
    genre: str
    permalink_url: AnyHttpUrl
    tag_list: str

    @classmethod
    def from_raw_hydration(
        cls,
        raw_hydration: str,
    ) -> Optional["SoundcloudTrack"]:
        hydration = json.loads(raw_hydration)
        assert isinstance(hydration, list)
        for object in hydration:
            item = SoundcloudHydrationItem(**object)
            if item.hydratable == "sound":
                assert isinstance(item.data, dict)
                return cls(**item.data)

    def comments(self) -> SoundcloudComments:
        return self._client.comments(self.id)
