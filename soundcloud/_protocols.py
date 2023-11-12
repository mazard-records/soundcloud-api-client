from abc import ABC, abstractmethod
from typing import Protocol, Union

from pydantic import AnyHttpUrl


class SoundcloudCommentsProtocol(ABC):
    pass


class SoundcloudTrackProtocol(ABC):
    @abstractmethod
    def comments(self) -> SoundcloudCommentsProtocol:
        pass


class SoundcloudClientProtocol(Protocol):
    def track(
        self,
        track_id_or_url: Union[int, str],
    ) -> SoundcloudTrackProtocol:
        pass

    def comments(self, track_id: int) -> SoundcloudCommentsProtocol:
        pass
