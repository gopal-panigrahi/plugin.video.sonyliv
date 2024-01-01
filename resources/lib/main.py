# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from resources.lib.constants import URLS
from resources.lib.api import SonyLivAPI
from resources.lib.builder import Builder
import urlquick
from codequick import Route, run, Script, Resolver, Listitem
from codequick.script import Settings


@Route.register
def root(_):
    yield Listitem.search(Route.ref("/resources/lib/main:list_tray"), url="search")
    yield from builder.build_menu()


@Route.register
def list_page(_, **kwargs):
    if "id" in kwargs:
        rel_url = URLS.get("PAGE").format(page_id=kwargs.get("id"))
        while True:
            page = api.get_page(rel_url, kwargs["start"], kwargs["end"])
            if len(page.get("containers")) == 0:
                break
            kwargs["start"] += kwargs["pageSize"]
            kwargs["end"] += kwargs["pageSize"]
            yield from builder.build_page(page.get("containers"))
    else:
        yield False


@Route.register
def list_tray(_, **kwargs):
    if kwargs.get("search_query", False):
        keyword = kwargs.get("search_query")
        items = api.get_search_response(keyword)
        yield from builder.build_tray(items)
    else:
        if "uri" in kwargs:
            tray = api.get_tray(kwargs.get("uri"), kwargs["start"], kwargs["end"])
            yield from builder.build_tray(tray.get("containers"))

            kwargs["total"] = tray.get("total")
            yield from builder.build_navigations(**kwargs)
        else:
            yield False


@Route.register(redirect_single_item=True)
def list_seasons(_, **kwargs):
    if "id" in kwargs:
        rel_url = URLS.get("SHOW").format(show_id=kwargs.get("id"))
        seasons = api.get_seasons(rel_url).get("containers")
        yield from builder.build_seasons(seasons)
    else:
        yield False


@Route.register
def list_episodes(_, **kwargs):
    if "id" in kwargs:
        sort_order = "desc"
        rel_url = URLS.get("SEASON").format(season_id=kwargs.get("id"))
        start = kwargs.get("start", 0)
        end = kwargs.get("end", 14)
        episodes = api.get_episodes(rel_url, start, end, sort_order)
        total = episodes.get("total")
        episodeCount = episodes.get("episodeCount")
        if total == 15 and ((start + 15) < episodeCount):
            yield Listitem().next_page(
                **{"id": kwargs.get("id"), "start": start + 15, "end": end + 15}
            )
        yield from builder.build_episodes(episodes.get("containers"))
    else:
        yield False


@Resolver.register
def play_video(_, **kwargs):
    if "video_id" in kwargs and "label" in kwargs:
        video_id = kwargs.get("video_id")
        label = kwargs.get("label")
        video_value = kwargs.get("video_value")
        is_preview_enabled = kwargs.get("is_preview_enabled")

        if video_value != "Free" and not is_preview_enabled:
            Script.notify("Can't Play Premium", "")
            return False

        playback_url, subtitles = api.get_video(video_id, video_value)
        stream_headers = api._get_play_headers()
        return builder.build_play(playback_url, stream_headers, label, subtitles)


@Script.register
def cleanup(_):
    urlquick.cache_cleanup(-1)
    Script.notify("Cache Cleaned", "")


api = SonyLivAPI()
builder = Builder()
