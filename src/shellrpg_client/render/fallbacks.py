from enum import Enum

class MediaMode(str, Enum):
    ANIMATED = "animated"
    STATIC = "static"
    ANSI = "ansi"
    ASCII = "ascii"
    TEXT = "text"
    STATUS_ONLY = "status_only"

def choose_media_mode(
    ansi_supported: bool,
    unicode_supported: bool,
    media_supported: bool,
    columns: int,
) -> MediaMode:
    if media_supported and columns >= 100:
        return MediaMode.ANIMATED
    if ansi_supported and unicode_supported and columns >= 80:
        return MediaMode.ANSI
    if columns >= 60:
        return MediaMode.ASCII
    if columns >= 40:
        return MediaMode.TEXT
    return MediaMode.STATUS_ONLY
