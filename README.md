# ***A**ural*

*A*ural is a **HIGHLY IN DEVELOPMENT** tool designed to manage music within a folder from the terminal. Featuring a suite of tools from altering metadata of files to simply downloading Youtube videos as `.mp3` in the best quality.

This tool relies on [yt-dlp](https://github.com/yt-dlp/yt-dlp) to
download audio files, and [mutagen](https://github.com/quodlibet/mutagen) for metadata editing. Definitely do go check both of them out.


### Possible Features to Add
| Feature                  | Description                                                                                                                                    |
| :----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Caching                  | Unknown if it's needed, but I will end up benchmarking the tool with large quantities of audio files at some point for testing.                |
| Textual UI Music Manager | Instead of a graphical ui (dearpygui) maybe a keyboard-controlled TUI would be nicer, instead of typing terminal commands each time for stuff. |

The goal of this project is a simple terminal interface for managing music inside a filesystem.

---
[LICENSE](./LICENSE) -
Built with [Python 3.13.5](https://www.python.org/downloads/release/python-3135)