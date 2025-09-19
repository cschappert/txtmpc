from mpd import MPDClient
from mpd_protocols import MPDCommandsProtocol
from typing import cast

def main():
    # TODO: Currently using a protocol so that type checking and autocompletion on
    # Runtime generated methods works. This is basically working, but it woudld be nice
    # not to have to switch between MPDClient and MPDCommandsProtocol based on whether I am
    # calling a method or just setting a variable.

    client = MPDClient()
    client.timeout = 10                 # network timeout in seconds (floats allowed), default: None
    client.idletimeout = None           # timeout for fetching the result of the idle command is handled seperately, default: None
    protocol = cast(MPDCommandsProtocol, client)
    protocol.connect("localhost", 6600)   # connect to localhost:6600

    print("MPD Status:")
    status = protocol.status()
    for key, value in status.items():
        print(f"{key}: {value}")

    print("\nCurrent Song:")
    current_song = protocol.currentsong()
    for key, value in current_song.items():
        print(f"{key}: {value}")

    print("\nPlaylist:")
    playlist = protocol.playlistinfo()
    for song in playlist:
        print(f"{song.get('pos', 'N/A')}: {song.get('title', 'Unknown Title')} by {song.get('artist', 'Unknown Artist')}")

    protocol.close()                      # send the close command
    protocol.disconnect()                 # disconnect from the server

main()
