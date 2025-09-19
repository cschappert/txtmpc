# txtmpc: Textual MPD Client

A terminal-based music client for MPD, built with Textual.

## Warning

I've just gotten started on this. Nothing works.

## Features
- Browse and play your local MPD library
- Optional Qobuz integration (browse/search/play Qobuz tracks)
- Tabbed interface for switching between local library and Qobuz

## Note

- txtmpc is **not** a way to gain access to Qobuz without a paid subscription
- txtmpc is **not** a way to download audio files that were not intended for download

## Requirements
- Python 3.12+ (Older versions of Python 3 may or may not work)
- MPD server
- (Optional) A paid Qobuz subscription

## Setup
1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage
Run the main application
(make sure you are still in the virtual environment):
```bash
python main.py
```

When you are finished, you can leave the virtual environment with:
```bash
deactivate
```

## License
MIT
