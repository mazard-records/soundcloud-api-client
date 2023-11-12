# soundcloud-api-client

[![tests](https://github.com/mazard-records/soundcloud-api-client/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/mazard-records/soundcloud-api-client/actions/workflows/tests.yaml)

> To be documented

```python
from soundcloud import SoundcloudClient

client = SoundcloudClient()
track = client.track("")
comments = track.comments()
for comment in comments:
    print(comment.body)
```