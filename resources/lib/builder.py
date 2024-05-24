# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from resources.lib.utils import deep_get, getThumbnail, getPoster, isPremium
from resources.lib.constants import CHANNELS, URLS
from codequick import Listitem, Resolver, Route
from codequick.script import Settings
import inputstreamhelper
from urllib.parse import urlencode
import time
from uuid import uuid4
import xbmc


class Builder:
    def buildMenu(self):
        for channel_name, channel_id, image in CHANNELS:
            item_data = {
                "callback": Route.ref("/resources/lib/main:list_page"),
                "label": channel_name,
                "params": {
                    "id": channel_id,
                    "start": 0,
                    "end": 9,
                    "pageSize": 10,
                },
            }
            item = Listitem.from_dict(**item_data)
            item.art.local_thumb(image)
            yield item

    def buildPage(self, page):
        for each in page:
            containers = deep_get(each, "assets.containers")
            if each.get("layout") == "portrait_layout" and len(containers) > 0:
                item_data = {
                    "callback": Route.ref("/resources/lib/main:list_tray"),
                    "label": deep_get(each, "metadata.label"),
                    "art": {
                        "thumb": getThumbnail(containers[0]),
                        "fanart": getPoster(containers[0]),
                    },
                    "info": {
                        "plot": deep_get(each, "metadata.listing_page_footer_desc"),
                    },
                    "params": {
                        "uri": URLS.get("TRAY") + deep_get(each, "retrieveItems.uri"),
                        "start": 0,
                        "end": 14,
                        "pageSize": 15,
                    },
                }
                yield Listitem.from_dict(**item_data)

    def buildTray(self, tray):
        for each in tray:
            contentType = deep_get(each, "metadata.objectSubtype")

            if contentType in ["SHOW", "EPISODIC_SHOW"]:
                yield self.buildShow(each)
            elif contentType in ["MOVIE", "TRAILER", "EPISODE", "CLIP"]:
                yield self.buildVideo(each)

    def buildShow(self, show):
        callback = Route.ref("/resources/lib/main:list_seasons")
        if deep_get(show, "metadata.contentSubtype") == "EPISODIC_SHOW":
            callback = Route.ref("/resources/lib/main:list_episodes")

        item_data = {
            "callback": callback,
            "label": deep_get(show, "metadata.title"),
            "art": {
                "thumb": getThumbnail(show),
                "fanart": getPoster(show),
            },
            "info": {
                "genre": deep_get(show, "metadata.genres"),
                "year": deep_get(show, "metadata.emfAttributes.release_year"),
                "plot": deep_get(show, "metadata.longDescription"),
                "plotoutline": deep_get(show, "metadata.shortDescription"),
            },
            "params": {"id": show.get("id")},
        }
        return Listitem.from_dict(**item_data)

    def buildVideo(self, video):
        premium = isPremium(video)
        item_data = {
            "callback": Resolver.ref("/resources/lib/main:play_video"),
            "label": f'{deep_get(video, "metadata.title")} {premium}',
            "art": {
                "thumb": getThumbnail(video),
                "fanart": getPoster(video),
            },
            "info": {
                "genre": deep_get(video, "metadata.genres"),
                "year": deep_get(video, "metadata.emfAttributes.release_year"),
                "plot": deep_get(video, "metadata.longDescription"),
                "plotoutline": deep_get(video, "metadata.shortDescription"),
            },
            "params": {
                "video_id": video.get("id"),
                "label": deep_get(video, "metadata.title"),
                "video_value": deep_get(video, "metadata.emfAttributes.value"),
                "is_preview_enabled": deep_get(
                    video, "metadata.emfAttributes.is_preview_enabled"
                ),
            },
        }
        return Listitem.from_dict(**item_data)

    def buildSeasons(self, seasons):
        for each in seasons[::-1]:
            item_data = {
                "callback": Route.ref("/resources/lib/main:list_episodes"),
                "label": deep_get(each, "metadata.title"),
                "art": {
                    "thumb": "",
                    "fanart": "",
                },
                "params": {"id": each.get("id")},
            }
            item = Listitem.from_dict(**item_data)
            item.art.local_thumb("season.png")
            yield item

    def buildEpisodes(self, episodes):
        playlist.clear()
        for each in episodes:
            premium = isPremium(each)
            item_data = {
                "callback": Resolver.ref("/resources/lib/main:play_video"),
                "label": f"Ep {deep_get(each, 'metadata.episodeNumber')}. {deep_get(each, 'metadata.episodeTitle')} {premium}",
                "art": {
                    "thumb": deep_get(each, "metadata.emfAttributes.thumbnail"),
                },
                "info": {
                    "genre": deep_get(each, "metadata.genres"),
                    "plot": deep_get(each, "metadata.longDescription"),
                    "plotoutline": deep_get(each, "metadata.shortDescription"),
                    "episode": deep_get(each, "metadata.episodeNumber"),
                    "duration": deep_get(each, "metadata.duration"),
                    "country": deep_get(each, "metadata.country"),
                    "cast": [deep_get(each, "metadata.emfAttributes.cast_and_crew")],
                    "aired": datetime.fromtimestamp(
                        deep_get(each, "metadata.originalAirDate") / 1000.0
                    ).strftime("%Y-%m-%d")
                    if deep_get(each, "metadata.originalAirDate")
                    else "",
                    "season": deep_get(each, "metadata.season"),
                },
                "params": {
                    "video_id": each.get("id"),
                    "label": deep_get(each, "metadata.episodeTitle"),
                    "video_value": deep_get(each, "metadata.emfAttributes.value"),
                    "is_preview_enabled": deep_get(
                        each, "metadata.emfAttributes.is_preview_enabled"
                    ),
                },
            }
            item = Listitem.from_dict(**item_data)
            playlist.add(item.listitem.getPath(), item.listitem, 0)
            yield item

    def buildNavigations(self, **kwargs):
        if kwargs.get("end") < kwargs.get("total"):
            kwargs["start"] += kwargs.get("pageSize")
            kwargs["end"] += kwargs.get("pageSize")
            yield Listitem().next_page(**kwargs)

    def buildPlay(self, playback_url, stream_headers, label, subtitles):
        is_helper = inputstreamhelper.Helper("mpd", drm=False)
        stream_headers.update(
            {
                "x-playback-session-id": "%s-%d" % (uuid4().hex, time.time() * 1000),
                "content-type": "application/octet-stream",
            }
        )

        if Settings.get_string("quality") == "Ask Quality":
            stream_selection_type = "ask-quality"
            resolution = ""
        else:
            stream_selection_type = "adaptive"
            resolution = Settings.get_string("quality")

        if is_helper.check_inputstream():
            item_data = {
                "callback": playback_url,
                "label": label,
                "properties": {
                    "IsPlayable": True,
                    "inputstream": is_helper.inputstream_addon,
                    "inputstream.adaptive.manifest_type": "mpd",
                    "inputstream.adaptive.license_type": False,
                    "inputstream.adaptive.stream_selection_type": stream_selection_type,
                    "inputstream.adaptive.chooser_resolution_max": resolution,
                    "inputstream.adaptive.chooser_resolution_secure_max": resolution,
                    "inputstream.adaptive.stream_headers": urlencode(stream_headers),
                    "inputstream.adaptive.manifest_headers": urlencode(stream_headers),
                    "inputstream.adaptive.license_key": "|%s|R{SSM}|"
                    % urlencode(stream_headers),
                },
                "subtitles": subtitles,
            }
            yield Listitem(content_type="video").from_dict(**item_data)


playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
