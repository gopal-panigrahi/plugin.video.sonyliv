from functools import reduce
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def is_premium(item):
    video_value = deep_get(item, "metadata.emfAttributes.value")
    is_preview_enabled = deep_get(item, "metadata.emfAttributes.is_preview_enabled")
    if video_value != "Free" and not is_preview_enabled:
        return "(Premium)"
    return ""


def update_query_params(url, params):
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlunparse(url_parts)


def get_thumbnail(item):
    images = [
        "square_thumb",
        "circular_image",
        "portrait_thumb",
        "masthead_background_mobile",
        "detail_cover_bg_mobile",
        "thumbnail",
    ]
    for image in images:
        img_url = deep_get(item, f"metadata.emfAttributes.{image}")
        if img_url:
            return img_url
    return get_poster(item)


def get_poster(item):
    images = [
        "landscape_thumb",
        "thumbnail",
        "masthead_background",
        "detail_cover_bg_mobile_v2",
        "detail_cover_bg_V2",
        "detail_cover_bg",
    ]
    for image in images:
        img_url = deep_get(item, f"metadata.emfAttributes.{image}")
        if img_url:
            return img_url
    return None
