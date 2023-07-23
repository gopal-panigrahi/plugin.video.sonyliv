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
    ("Home", "33958"),
    ("TV Shows", "2240"),
    ("New", "159701"),
    ("Movies", "399"),
    ("Originals", "5193"),
    ("Watch free", "109623"),
]

URLS = {
    "TOKEN": "/AGL/1.4/A/ENG/WEB/ALL/GETTOKEN",
    "PAGE": "/AGL/2.6/A/ENG/WEB/IN/MH/PAGE/{page_id}?kids_safe=false",
    "TRAY": "/AGL/2.6/A/ENG/WEB/IN/MH",
    "SHOW": "/AGL/2.4/A/ENG/WEB/IN/MH/DETAIL/{show_id}",
    "SEASON": "/AGL/2.6/A/ENG/WEB/IN/MH/CONTENT/DETAIL/BUNDLE/{season_id}?&kids_safe=false&orderBy=episodeNumber",
    "VIDEO": "/AGL/1.5/A/ENG/WEB/IN/CONTENT/VIDEOURL/VOD/{video_id}",
    "VIDEO_PREVIEW": "/AGL/1.5/A/ENG/WEB/IN/CONTENT/VIDEOURL/VOD/{video_id}/freepreview",
}