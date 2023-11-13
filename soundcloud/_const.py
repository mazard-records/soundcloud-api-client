import re

DEFAULT_API_URL = "https://api-v2.soundcloud.com"
DEFAULT_FRONT_URL = "https://soundcloud.com"

PATTERN_SRCS = re.compile(r"<script crossorigin src=\"([^\"]+)\">")
PATTERN_HYDRATE = re.compile(r"window.__sc_hydration = (\[\{.+\}\]);")
PATTERN_VARIABLE = re.compile(r"\"client_id=([^\"]+)\"")
