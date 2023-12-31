# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.utils import deep_get, update_query_params
import urlquick
from resources.lib.constants import BASE_HEADERS, URLS, url_constructor
from codequick import Script


class SonyLivAPI:
    def __init__(self):
        self.reset_session()

    def _get_token(self):
        url = url_constructor(URLS.get("TOKEN"))
        resp = self.get(url)
        return deep_get(resp, "resultObj")

    def get_page(self, rel_url, start, end):
        url = update_query_params(rel_url, {"from": start, "to": end})
        url = url_constructor(url)
        resp = self.get(url)
        return resp.get("resultObj")

    def get_tray(self, rel_url, start, end):
        url = update_query_params(rel_url, {"from": start, "to": end})
        url = url_constructor(url)
        resp = self.get(url)
        return deep_get(resp, "resultObj")

    def get_seasons(self, rel_url):
        url = url_constructor(rel_url)
        resp = self.get(url)
        seasons = deep_get(resp, "resultObj.containers")[0]
        return seasons

    def get_episodes(self, rel_url, start, end, sort_order):
        url = update_query_params(
            rel_url, {"from": start, "to": end, "sortOrder": sort_order}
        )
        url = url_constructor(url)
        resp = self.get(url)
        episodes = deep_get(resp, "resultObj.containers")[0]
        return episodes

    def get_video(self, video_id, video_value):
        if video_value == "Free":
            url = url_constructor(URLS.get("VIDEO").format(video_id=video_id))
        else:
            url = url_constructor(URLS.get("VIDEO_PREVIEW").format(video_id=video_id))
        resp = self.get(url)
        video_url = deep_get(resp, "resultObj.videoURL")
        subtitles = [
            sub.get("subtitleUrl") for sub in deep_get(resp, "resultObj.subtitle")
        ]
        return video_url, subtitles

    def get_search_response(self, keyword):
        url = update_query_params(URLS.get("SEARCH"), {"query": keyword})
        url = url_constructor(url)
        resp = self.get(url)
        search_result = []
        for item in deep_get(resp, "resultObj.containers")[0].get("containers"):
            search_result.extend(item.get("assets"))
        return search_result

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url, **kwargs)
            return response.json()
        except Exception as e:
            self.reset_session()
            return self._handle_error(e, url, "get", **kwargs)

    def post(self, url, **kwargs):
        try:
            response = self.session.post(url, **kwargs)
            return response.json()
        except Exception as e:
            self.reset_session()
            return self._handle_error(e, url, "post", **kwargs)

    def _handle_error(self, e, url, _rtype, **kwargs):
        Script.notify("Internal Error", "")

    def reset_session(self):
        self.session = urlquick.Session()
        self.session.headers.update(BASE_HEADERS)
        security_token = self._get_token()
        self.session.headers.update({"security_token": security_token})

    def _get_play_headers(self):
        stream_headers = self.session.headers
        return stream_headers
