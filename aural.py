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
    """
    Returns `True` if the `url` is a valid `url`.
    Does not check for specific domains, only if it's a valid url.
    """
    regex = (
        # To be honest, I ChatGippitied this regex.
        r"https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?"
    )
    return re.match(regex, url) is not None

def error(error_msg: str, quit: bool = True) -> None:
    print(f"{PROG_TAG} {error_msg}")
    if quit:
        exit()

def editMetaData(filename: str) -> None:
    print(filename)
    print(PROG_TAG, "EditMetaData")
    pass

def verifyProgramFolders() -> None:
    """
    Verifies that `FOLDER_TEMP` and `FOLDER_OUT` were created. If they weren't
    it creates them.
    """
    try:
        if not os.path.exists(FOLDER_TEMP):
            os.makedirs(FOLDER_TEMP)
        if not os.path.exists(FOLDER_OUT):
            os.makedirs(FOLDER_OUT)
    except Exception as e:
        error(e.__str__())

def download(url: str, out: str = "") -> None:
    """
    Returns `True` if the download was successful, `False` if not.
    """
    if not isValidURL(url):
        error(f"Invalid URL: {url}")

    # User did not provide an output name, so the creates one.
    if not out:
        out = os.path.join(FOLDER_TEMP, '%(title)s_temp.%(ext)s')

    # yt-dlp's download options, gets passed into the download function
    # Unknown if these are best settings for however, it makes sense to me
    # to have all files in `.mp3` format.
    download_options = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': out,
        'quiet': True,
        'noplaylist': True,
    }

    # actually attempt to download the music
    try:
        with ytdl(download_options) as ydl:
            ydl.download(url)
    except Exception as e:
        error(e.__str__())
    else:
        # move on to verifying metadata
        print(out)
        editMetaData(out)

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
    parser.add_argument("-m", "--metadata", nargs=1, type=str,
        help="edit the metadata of the file path specified"
    )

    args: argparse.Namespace = parser.parse_args()

    if args.url:
        download(args.url)

    if args.metadata:
        editMetaData(args.metadata)
    # 2. Download file to a staging folder.
    # 3. Set the metadata, or stick with default (if provided)
    # 4. Write file to a final folder.