from typing import TypeVar

from pydantic import AnyHttpUrl, BaseModel

from ._protocols import (
    SoundcloudClientProtocol,
    SoundcloudTrackProtocol,
)

M = TypeVar("M")


class BaseSoundcloudModel(BaseModel):
    """ Base model with id and uri attributes. """
    _client: SoundcloudClientProtocol
    id: int
    uri: AnyHttpUrl


class SoundcloudPaginableModel(BaseModel):
    """ Base container for paginable collection. """
    collection: list(M)
    next_href: AnyHttpUrl


class SoundcloudCommentModel(BaseSoundcloudModel):
    """ @see: 
    https://developers.soundcloud.com/docs/api/explorer/open-api#model-Comment
    """

    body: str
    timestamp: str

    track_id: int
    user_id: int


class SoundcloudCommentsModel(SoundcloudPaginableModel):
    """ @see: 
    https://developers.soundcloud.com/docs/api/explorer/open-api#model-Comments
    """

    collection: list(SoundcloudCommentModel)


class SoundcloudTrack(BaseSoundcloudModel, SoundcloudTrackProtocol):
    """ @see: 
    https://developers.soundcloud.com/docs/api/explorer/open-api#model-Track
    """

    title: str
    artwork_url: AnyHttpUrl
    duration: int
    genre: str
    isrc: str
    key_signature: str
    permalink_url: AnyHttpUrl
    tag_list: str

    def comments(self) -> SoundcloudCommentsModel:
        return self._client.comments(self.id)
