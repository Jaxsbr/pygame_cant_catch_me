# Can't catch me

This is tile base game with two actors, a player (you) and an enemy.

The enemy moves once every 2 times the player moves.

The player wins the game by:
- Avoiding the enemy
- Collecting a key
- Reaching the exit

The player loses the game when the enemy get close the the player.


## Run locally

First create a virtual environment

`python3 -m venv myvenv`

Activate the virtual environment

`source myvenv/bin/activate`

Install dependencies

`pip install -r requirements.txt`

Run

`python3 main.py`


## How to put the game on ubuntu

Create a desktop file

`nano ~/Desktop/game_name.desktop`

Add the following content.
Be sure the update the paths properly for your system.
```yaml
[Desktop Entry]
Version=1.0
Name=Game Name
Exec=bash -c "python3 -m venv myvenv && source /location/of/code/myvenv/bin/activate && pip install -r requirements.txt && /usr/bin/python3 /location/of/code/main.py"
Terminal=false
Type=Application
Path=/location/of/code
```

`Exec`: We launch the game using `bash` in order to chain commands. These are the same commands defined in the [Run Locally](#run-locally) section above

`Path`: To access files and images the game needs to know where assets are located

Once the .desktop file is run, you might encounter security/permission issues.
Simply follow the ubuntu recommendation that pop up when launching from the desktop icon.
e.g.
- `Allow Launching` - from the right click context menu
- `Allow executing file as program` - from the right click context menu, find properties, find permission
