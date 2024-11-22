# Game Name

This is a Python game designed to be easy to set up and play on an Ubuntu laptop. Follow these steps to install and play the game.

---

## Requirements
- An Ubuntu laptop (or another Linux-based system).
- Basic familiarity with copying and running files.

---

## Instructions

### 1. Install Necessary Tools

1. Open a terminal.
2. Update the system and install Python (if not already installed):
    ```
    sudo apt update
    sudo apt install python3 python3-pip
    ```
3. Install `pyinstaller`:
    ```
    pip3 install pyinstaller
    ```

---

### 2. Build the Executable

1. Transfer the game code file (`your_game.py`) to the Ubuntu laptop. You can use a USB drive, email, or cloud storage.
2. Open a terminal and navigate to the folder containing `your_game.py`.
3. Run this command to create a standalone executable:
    ```
    pyinstaller --onefile your_game.py
    ```
4. After the process completes, the executable will be located in the `dist/` folder:
    - Example path: `dist/your_game`

---

### 3. Run the Game

1. Move the executable file to an easy-to-access location, such as `~/Games/`.
2. Make the file executable by running:
    ```
    chmod +x ~/Games/your_game
    ```
3. Run the game by double-clicking the executable or entering:
    ```
    ./your_game
    ```

---

### 4. (Optional) Create a Desktop Shortcut

1. Open a terminal and create a launcher file:
    ```
    nano ~/.local/share/applications/your_game.desktop
    ```
2. Add the following content to the file:
    ```
    [Desktop Entry]
    Name=Your Game
    Exec=/path/to/your_game
    Type=Application
    Terminal=false
    ```
3. Save and close the file.
4. Make the shortcut executable:
    ```
    chmod +x ~/.local/share/applications/your_game.desktop
    ```
5. Your game will now appear in the application menu for easy launching.

---

## Testing

Run the game to ensure everything works as expected. Verify that all required assets (like images and sounds) are included and that file paths in the code are correctly set.

---

Enjoy the game!
