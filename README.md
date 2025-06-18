# Steam Shortcut Automation Program

Steam Shortcut Automation Program (SteamSAP) helps SteamOS users add web apps or cloud gaming URLs as shortcuts in the Steam library. It backs up existing entries, handles user-agent spoofing, and launches browsers via Flatpak.

## Prerequisites
- SteamOS or a Linux distribution with Steam installed
- Python 3.8+
- Flatpak with Chrome, Edge or Firefox installed

## Installation
Clone this repository and ensure `user_agents.json` is in the same directory as `main.py`.

```
python3 -m pip install -r requirements.txt  # if requirements are added
```

## Usage
Run the program with Python:

```
python3 main.py
```

Use the GUI to add titles and URLs, choose a browser and optional user agent, then save the shortcuts to Steam. Steam may need a restart for the shortcuts to appear.

## License
This project is released under the MIT License.
