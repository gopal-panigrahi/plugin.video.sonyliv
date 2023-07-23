# -*- coding: utf-8 -*-
from codequick.utils import urljoin_partial

# URLs
API_BASE_URL = "https://apiv2.sonyliv.com"

BASE_HEADERS = {
    "content-type": "application/json",
    "x-via-device": "true",
    "app_version": "3.3.58",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7",
    "cache-control": "no-cache",
    "origin": "https://www.sonyliv.com",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
}

url_constructor = urljoin_partial(API_BASE_URL)

CHANNELS = [
    ("Home", "33958", "home.png"),
    ("TV Shows", "2240", "tv.png"),
    ("New", "159701", "new.png"),
    ("Movies", "399", "movies.png"),
    ("Originals", "5193", "originals.png"),
    ("Watch free", "109623", "free.png"),
]

URLS = {
    "TOKEN": "/AGL/1.4/A/ENG/WEB/ALL/GETTOKEN",
    "PAGE": "/AGL/2.6/A/ENG/WEB/IN/MH/PAGE/{page_id}?kids_safe=false",
    "TRAY": "/AGL/2.6/A/ENG/WEB/IN/MH",
    "SEARCH": "/AGL/2.9/A/ENG/WEB/IN/MH/TRAY/SEARCH?from=0&to=12&app_version=3.10.3&kids_safe=false",
    "SHOW": "/AGL/2.4/A/ENG/WEB/IN/MH/DETAIL/{show_id}",
    "SEASON": "/AGL/2.6/A/ENG/WEB/IN/MH/CONTENT/DETAIL/BUNDLE/{season_id}?&kids_safe=false&orderBy=episodeNumber",
    "VIDEO": "/AGL/1.5/A/ENG/WEB/IN/CONTENT/VIDEOURL/VOD/{video_id}",
    "VIDEO_PREVIEW": "/AGL/1.5/A/ENG/WEB/IN/CONTENT/VIDEOURL/VOD/{video_id}/freepreview",
}
