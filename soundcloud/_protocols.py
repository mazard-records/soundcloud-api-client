from typing import Protocol, Union


class SoundcloudTrackProtocol(Protocol):
    ...


class SoundcloudClientProtocol(Protocol):

    def track(
        self,
        track_id_or_url: Union[int, str],
    ) -> SoundcloudTrackProtocol:
        pass

    def comments(self, track_id: int) -> ...:
        pass
