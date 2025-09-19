from typing import cast

from mpd import CommandError, MPDClient
from textual.app import App, ComposeResult
from textual.events import Mount
from textual.widgets import (DataTable, Footer, ListItem, ListView, Static,
                             TabbedContent, TabPane)

from mpd_protocols import MPDCommandsProtocol


class PlaylistWidget(DataTable):
    """A browsable playlist for the current MPD queue."""


class TxtmpcApp(App):

    CSS_PATH = "txmpc.css"
    BINDINGS = [
        ("1", "show_tab('playlist')", "Playlist"),
        ("2", "show_tab('library')", "Library"),
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None
        self.protocol = cast(MPDCommandsProtocol, self.client)
        self.protocol.connect("localhost", 6600)

        table = self.query_one(PlaylistWidget)
        table.add_columns("Artist", "Track", "Title", "Album", "Time")
        table.cursor_type = "row"
        table.focus()

        playlist = self.protocol.playlistinfo()
        table.clear()
        for song in playlist:
            title = song.get("title", "Unknown Title")
            artist = song.get("artist", "Unknown Artist")
            album = song.get("album", "Unknown Album")
            time = song.get("time", "0")
            minutes = int(time) // 60
            seconds = int(time) % 60
            time = f"{minutes}:{seconds:02}"
            track = song.get("track", "N/A")
            id = song.get("id")

            table.add_row(artist, track, title, album, time, key=id)

    def compose(self) -> ComposeResult:
        """Compose app with tabbed content."""
        # Footer to show keys
        yield Footer()

        # Add the TabbedContent widget
        with TabbedContent(initial="playlist"):
            with TabPane("Playlist", id="playlist"):  # First tab
                yield PlaylistWidget()
            with TabPane("Library", id="library"):
                yield Static("Library Tab (to be implemented)")

    def action_show_tab(self, tab: str) -> None:
        """Switch to a new tab."""
        self.get_child_by_type(TabbedContent).active = tab
        table = self.query_one(PlaylistWidget)
        table.focus()

    def on_unmount(self) -> None:
        """Disconnect from MPD when the widget is unmounted."""
        self.protocol.close()
        self.protocol.disconnect()


if __name__ == "__main__":
    app = TxtmpcApp()
    app.run()
