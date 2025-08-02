#!/usr/bin/env python3

# This is a rewrite (kinda) of the `graphical.py` code. Sometimes a rewrite is
# needed you know? This is meant to be more thought out, before it was just
# slop code with barely any comments that just worked. I disliked it though,
# oh perfectionism, gotta love it.
#
# Dearpygui is cool and all, but it's got clutter code that doesn't look good.
# Python in general doesn't look that fancy to me though. Plus, a graphical UI
# takes forever with having to use the mouse (oh, I use vim btw).
#
# This code falls under the GNU GPL v3.0 License

from typing import Optional
from yt_dlp import YoutubeDL as ytdl
import argparse  # parsin' arrrrrgs
import mutagen   # library for reading/writing to .mp3 files
import os        # renaming, path joining
import re        # regex capabilites for detecting a valid URL

FOLDER_TEMP = "./temp"
FOLDER_OUT  = "./jams"

PROG_AUTHOR = "komidan"
PROG_TAG    = "[AURAL]"
PROG_VER    = "v0.1.0"

def isValidURL(url: str) -> bool:
    regex = (
        # To be honest, I ChatGippitied this regex.
        r"https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?"
    )
    return re.match(regex, url) is not None

def log(log: str) -> None:
    print(f"{PROG_TAG} LOG:  {log}")

def warn(warn_msg: str) -> None:
    print(f"{PROG_TAG} WARN: {warn_msg}")

def error(error_msg: str, quit: bool = True) -> None:
    print(f"{PROG_TAG} ERR:  {error_msg}")
    if quit:
        exit()

def verifyProgramFolders() -> None:
    try:
        if not os.path.exists(FOLDER_TEMP):
            os.makedirs(FOLDER_TEMP)
        if not os.path.exists(FOLDER_OUT):
            os.makedirs(FOLDER_OUT)
    except Exception as e:
        error(e.__str__())

def editMetaData(filename: str) -> None:
    print(PROG_TAG, f"EditMetaData ['{filename}']")
    pass

def download(url: str) -> str:
    """
    Downloads a file and returns the file path of downloaded file
    """
    if not isValidURL(url):
        error(f"Invalid URL: {url}")

    log(f"Starting Download on {url}")

    download_options: dict[str, object] = {

        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(FOLDER_TEMP, '%(title)s.%(ext)s'),
        # 'quiet': True,
        'noplaylist': True,
    }
    filepath: str = ""

    # attempt to download the music
    try:
        with ytdl(download_options) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title') # type: ignore | Pylance, really?

            # Should always be .mp3, if not idk
            if not title:
                warn("Failed to get video title")
            filepath = os.path.join(FOLDER_TEMP, f"{title}.mp3")
    except Exception as e:
        error(e.__str__())

    if not os.path.exists(filepath):
        error("Download was successful, but output is missing? You can manually edit the metadata using `aural.py -m (filepath)`")

    log(f"Download successful")
    return filepath

if __name__ == '__main__':
    # This if statement prevents this code from executing if this file was
    # included externally. It serves as the main program logic for running this
    # from the terminal.
    parser = argparse.ArgumentParser(
        prog="Aural",
        description="terminal-based file system music manager",
        epilog="link: https://github.com/komidan/aural"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {PROG_VER}")
    parser.add_argument("url", nargs="?",
        help="provided url to download using yt-dlp"
    )
    parser.add_argument("-o", "--output", type=str, default="",
        help="set a custom output name of the destination file"
    )
    parser.add_argument("-m", "--metaedit", type=str,
        help="this argument accepts a file path that will execute the metadata editor on the given file, no need to pass a URL in this case"
    )
    args: argparse.Namespace = parser.parse_args()

    # yt-dlp's download options, gets passed into the download function
    # Unknown if these are best settings for however, it makes sense to me
    # to have all files in `.mp3` format.

    try:
        if args.url:
            file = download(args.url)
            editMetaData(file)
            if args.output:
                print(args.output)
        if args.metaedit:
            editMetaData(args.metaedit)

    except Exception as e:
        error(e.__str__())


    # 2. Download file to a staging folder.
    # 3. Set the metadata, or stick with default (if provided)
    # 4. Write file to a final folder.