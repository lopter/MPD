# Copyright 2019 The Music Player Daemon Project
# http://www.musicpd.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# NOTE:
#
# This module is highly inspired from the youtube-dl plugin in mpv and actually
# implements mpv's edl:// URL scheme for adaptive streaming.

import argparse
import logging
import sys
try:
    import youtube_dl
except Exception as ex:
    print(
        "{}: could not import youtube_dl ({}), is it installed "
        "correctly?".format(sys.argv[0], ex)
    )
    sys.exit(1)

from typing import (
    Any,
    Dict,
    Union,
)

YTDL_BASE_OPTS: Dict[str, Any] = {
    "extract_flat": "in_playlist",  # --flat-playlist
    "format": "bestaudio/best",
    "logger": logging.getLogger("YoutubeDL"),
    "noplaylist": True,
    "socket_timeout": 10,
    "usenetrc": True,
}


logger = logging.getLogger("main")


def extract_info(input_url: str) -> Union[None, Dict[str, Any]]:
    ytdl_opts = YTDL_BASE_OPTS.copy()
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        try:
            return ytdl.extract_info(input_url, download=False)
        except youtube_dl.utils.UnavailableVideoError:
            logger.error("The requested file is not available")
        except youtube_dl.utils.MaxDownloadsReached:
            logger.error("You have reached your download quota for that site")
    return None


def rewrite_url(ytdl_info: Dict[str, Any]) -> Union[None, str]:
    output_url = ytdl_info.get("url")
    if output_url is None:
        logger.error("Couldn't process ytdl info for {}".format(
            ytdl_info.get("webpage_url")
        ))
    return output_url


def main() -> None:
    opts_parser = argparse.ArgumentParser(
        description="YoutubeDL integration glue for internal use by MPD",
    )
    opts_parser.add_argument(
        "-v", "--verbosity",
        default="error",
        choices=["debug", "info", "warning", "error"],
    )
    opts_parser.add_argument("input_url")
    opts = opts_parser.parse_args(sys.argv[1:])

    logging.basicConfig(
        format="mpd-ytdl[{levelname}]: {message}",
        style="{",
        level=opts.verbosity.upper(),
    )

    ytdl_info = extract_info(opts.input_url)
    if ytdl_info is None:
        sys.exit(1)
    output_url = rewrite_url(ytdl_info)
    if output_url is None:
        sys.exit(1)
    print(output_url)
    sys.exit(0)
