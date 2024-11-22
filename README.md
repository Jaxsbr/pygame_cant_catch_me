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

`python3 app/main.py`


## How to put the game on ubuntu

Create a desktop file

`nano ~/Desktop/game_name.desktop`

Add the following content.
Be sure the update the paths properly for your system.
```yaml
[Desktop Entry]
Version=1.0
Name=Game Name
Exec=bash -c "python3 -m venv myvenv && source /location/of/code/myvenv/bin/activate && pip install -r requirements.txt && /usr/bin/python3 /location/of/code/app/main.py"
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


## Attempt to make updating to latest game easier

```bash
#!/bin/bash

# Variables
ZIP_URL="https://github.com/Jaxsbr/pygame_cant_catch_me/archive/refs/heads/main.zip"
ZIP_FILE="/tmp/pygame_cant_catch_me_main.zip"
EXTRACT_DIR="/tmp/pygame_cant_catch_me_main"
GAME_DIR="/home/user/pygame_cant_catch_me-main"

# Step 1: Download the zip file
echo "Downloading the latest game files..."
curl -L -o "$ZIP_FILE" "$ZIP_URL"
if [ $? -ne 0 ]; then
    echo "Failed to download the zip file."
    exit 1
fi

# Step 2: Extract the content of the zip
echo "Extracting the zip file..."
unzip -q "$ZIP_FILE" -d "/tmp"
if [ $? -ne 0 ]; then
    echo "Failed to extract the zip file."
    rm -f "$ZIP_FILE"
    exit 1
fi

# Step 3: Delete the existing game directory content
echo "Deleting old game files..."
if [ -d "$GAME_DIR" ]; then
    rm -rf "$GAME_DIR"
fi

# Step 4: Create the parent directory for the game directory
echo "Ensuring destination directory exists..."
mkdir -p "$(dirname "$GAME_DIR")"

# Step 5: Move the extracted content into the game directory
echo "Copying new game files..."
mv "$EXTRACT_DIR" "$GAME_DIR"
if [ $? -ne 0 ]; then
    echo "Failed to move new game files."
    rm -rf "$EXTRACT_DIR"
    rm -f "$ZIP_FILE"
    exit 1
fi

# Step 6: Clean up temporary files
echo "Cleaning up..."
rm -rf "$EXTRACT_DIR"
rm -f "$ZIP_FILE"

echo "Update completed successfully!"

```
