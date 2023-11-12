import pytest

from soundcloud._front import get_client_id, get_track_id_from_url

TEST_URLS = (
    "https://soundcloud.com/cl-ment-dalibot/i-hate-models-nuits-sonores-lyon?in_system_playlist=personalized-tracks%3A%3Amazard-records%3A633133140",
    "https://soundcloud.com/cl-ment-dalibot/i-hate-models-nuits-sonores-lyon",
    "/cl-ment-dalibot/i-hate-models-nuits-sonores-lyon",
    "cl-ment-dalibot/i-hate-models-nuits-sonores-lyon",
)

async def test_get_client_id() -> None:
    client_id = await get_client_id()
    assert client_id is not None
    assert len(client_id) > 0


@pytest.mark.parametrize("url", TEST_URLS)
async def test_get_track_from_url(url: str) -> None:
    track_id = await get_track_id_from_url(url)
    assert track_id == 633133140
