#
# WARNING:
# This was a first-write and NOT that great. I'm in the process of rewriting
# the project having learned more about these libraries and wanting to remove
# the dearpygui library because keyboard only is best (vim user btw).
#
# This code might work on other operating systems because it's Python, but
# it hasen't been tested, don't trust it.
#

import dearpygui.dearpygui as dpg
from yt_dlp import YoutubeDL as ytdl
import time
import os
from mutagen.easyid3 import EasyID3
import re

WINDOW_HEIGHT = 800
WINDOW_WIDTH  = 600
DOWNLOAD_FOLDER = "./downloads"

def is_valid_youtube_url(url) -> bool:
    regex = (
        r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=[\w-]+|(?:[^/]+/)+[\w-]+)([^\s]*)$'
    )
    return re.match(regex, url) is not None

def download() -> None:
    url = dpg.get_value("url")

    if not is_valid_youtube_url(url):
        set_status("provide a valid url")
        return

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, 'temp.%(ext)s'),
        'quiet': True,
        'noplaylist': True,
    }

    # Verify folder exists
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    set_status("downloading")
    dpg.configure_item("loading_circle", show=True)
    dpg.set_value("url", "")
    try:
        with ytdl(ydl_opts) as ydl:
            ydl.download(url)

        set_status("download finished")
    except Exception as e:
        set_status("error; check console")
        print(e)
        return
    else:
        dpg.configure_item("loading_circle", show=False)
        metadata_editor(os.path.join(DOWNLOAD_FOLDER, "temp.mp3"))

def quit() -> None:
    dpg.stop_dearpygui()

def set_status(new_status: str = "") -> None:
    dpg.configure_item("status", label="test")
    dpg.set_value("status", f"[ {new_status} ]")

def save_metadata(file_path) -> None:
    # writes the meta data to file
    print(f"SAVING PROCESS: {file_path}")
    try:
        file = EasyID3(file_path)

        title = dpg.get_value("meta_title")
        artist = dpg.get_value("meta_artist")
        album = dpg.get_value("meta_album")

        file["title"] = title
        file["artist"] = artist
        file["album"] = album

        # TODO: ADD SUPPORT FOR ALBUM ART

    except Exception as e:
        set_status("error; check console")
        print(e)
    else:
        dpg.delete_item("metadata_editor")
        file.save()

        # rename the file to new fname
        fname = f"{artist} - {title}.mp3"
        os.rename(os.path.join(DOWNLOAD_FOLDER, os.path.basename(file_path)), os.path.join(DOWNLOAD_FOLDER, fname))

        # if os.path.exists(os.path.join(DOWNLOAD_FOLDER, "temp.mp3")):
        #     os.remove(os.path.join(DOWNLOAD_FOLDER, "temp.mp3"))

    set_status("saved file")

def get_metadata(file_name) -> None:
    try:
        file = EasyID3(file_name)

        title = file.get("title", [""])[0]       # type: ignore
        artist = file.get("artist", [""])[0]     # type: ignore
        album = file.get("album", [""])[0]       # type: ignore

        dpg.set_value("meta_title", value=title)
        dpg.set_value("meta_artist", value=artist)
        dpg.set_value("meta_album", value=album)

    except Exception as e:
        set_status("error; check console")
        print(f"SET_METADATA {e}")
        return

def file_selected(sender, app_data) -> None:
    # Handles file-dialog usage
    selected_path = app_data['file_path_name']
    if not os.path.exists(selected_path):
        set_status("select a path")
        return

    metadata_editor(selected_path)

def metadata_editor(file_path) -> None:
    # GUI for editing .mp3 metadata data
    file_name = os.path.basename(file_path)
    set_status("editing metadata")

    with dpg.window(label=f"Metadata Editor | {file_name}", tag="metadata_editor", no_close=True, width=450, height=550):
        dpg.add_input_text(label="title", tag="meta_title", hint="Alice in Wonderland", width=-120)
        dpg.add_input_text(label="artist", tag="meta_artist", hint="Tsubaki (feat. UX)", width=-120)
        dpg.add_input_text(label="album", tag="meta_album", width=-120)

        # extra metadata info
        size_mb = os.path.getsize(file_path) / (1024 * 1024)
        last_modified = time.ctime(os.path.getmtime(file_path))
        creation_date = time.ctime(os.path.getctime(file_path))

        dpg.add_text(f"size: {size_mb:.2f} MB")
        dpg.add_text(f"last modified: {last_modified}")
        dpg.add_text(f"creation date: {creation_date}")

        dpg.add_spacer()
        dpg.add_button(label="save", width=-1, tag="save_btn", callback=lambda: save_metadata(file_path))
        dpg.add_button(label="cancel/close", width=-1, callback=lambda: dpg.delete_item("metadata_editor"))

    get_metadata(file_path)

def main():
    with dpg.window(tag="primary", autosize=True, no_close=True, no_title_bar=True):
        with dpg.child_window(autosize_x=True, auto_resize_y=True):
            with dpg.group(horizontal=True):
                dpg.add_text(f"Music File Editor")
                dpg.add_text(f"[ awaiting ]", tag="status")

        with dpg.group(width=-1):
            dpg.add_input_text(
                hint="youtube link",
                width=-1,
                tab_input=False,
                no_spaces=True,
                tag="url"
            )
            dpg.add_button(label="download", tag="download", width=-1, callback=download)

        dpg.add_loading_indicator(
            show=False,
            style=1,
            circle_count=4,
            tag="loading_circle",
            indent=int(WINDOW_WIDTH / 2) - 32
        )

        with dpg.file_dialog(
                label="pick a file",
                default_path=DOWNLOAD_FOLDER,
                directory_selector=False,
                show=False,
                callback=file_selected,
                tag="file_picker",
                modal=True,
                height=600,
                width=500
            ):
            dpg.add_file_extension(".mp3", color=(150, 255, 150, 255))

        dpg.add_button(
            label="metadata editor",
            width=-1,
            tag="edit_btn",
            callback=lambda: dpg.show_item("file_picker")
        )
        dpg.add_button(label="exit", width=-1, tag="quit_btn")
        with dpg.popup(parent="quit_btn", modal=True, tag="quit_modal", mousebutton=dpg.mvMouseButton_Left):
            dpg.add_text("Are you sure you want to quit?")
            with dpg.group(horizontal=True, horizontal_spacing=10):
                dpg.add_button(label="yes", callback=quit)
                dpg.add_button(label="no", callback=lambda: dpg.configure_item("quit_modal", show=False))

if __name__ == '__main__':
    dpg.create_context()
    dpg.create_viewport(title="Music Saver", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    dpg.setup_dearpygui()

    main()
    dpg.set_primary_window("primary", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()