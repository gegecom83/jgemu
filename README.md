# jgemu

**jgemu** is a simple emulator launcher written in PyQt5.  
Its creation was inspired by [Yava](https://github.com/Beluki/Yava).

**Now supports both Windows and Linux!**

---

## Features

- Unified interface for launching games with different emulators
- Works on Windows and Linux
- Reads configuration from `config.ini`
- Keyboard shortcuts for quick navigation
- Recursively lists games from subdirectories
- Portable: no installation required

---

## Screenshots

![main](https://github.com/gegecom83/jgemu/blob/main/main.png)

---

## Installation

### Requirements

- Python 3.7+
- PyQt5

Install dependencies:

```sh
pip install PyQt5
```

---

## Usage

Place `jgemu.py`, your `config.ini`, and your icon (`icon.ico` for Windows, `icon.png` for Linux, optional) in the same directory.  
Then run:

```sh
python jgemu.py
```

---

## Configuration

`jgemu` is configured using a file named **`config.ini`**. This file contains everything jgemu needs to know about the folders and files it will launch.

Below are example configurations for **Windows** and **Linux**.  
**Use the appropriate path style and emulator executable for your OS.**

### Example `config.ini` for Windows

```ini
[Game Boy]
games       = C:\Games\Game Boy\
executable  = C:\Emulators\BGB\bgb.exe
extensions  = .zip, .gb
working_dir = 
preview_dir = C:\thumbnails\gb\snaps

[NEC PC Engine CD]
games       = D:\NEC PC Engine CD\
executable  = C:\Emulators\RetroArch\retroarch.exe
extensions  = .cue
parameters  = -L cores\mednafen_pce_libretro.dll
working_dir = C:\Emulators\RetroArch\
preview_dir = C:\thumbnails\pcenginecd\snaps

```

### Example `config.ini` for Linux

```ini
[Game Boy]
games       = /home/youruser/Games/GameBoy
executable  = /usr/bin/gambatte
extensions  = .zip, .gb
working_dir = /usr/bin
preview_dir = /home/youruser/thumbnails\gb\snaps

[NEC PC Engine CD]
games       = /mnt/storage/NEC_PC_Engine_CD
executable  = /usr/bin/retroarch
extensions  = .cue
parameters  = -L, /.config/retroarch/cores/mednafen_pce_libretro.so
working_dir = /usr/bin
preview_dir = /home/youruser/thumbnails\pcenginecd\snaps

```

#### Configuration Options

- **games**: Path to the folder containing ROMs/games.
- **executable**: Full path to emulator executable.
- **extensions**: Comma-separated list of file extensions to show (including the dot, e.g. `.zip, .gb`).
- **parameters** _(optional)_: Command-line parameters for the emulator, separated by commas.
- **working_dir** _(optional)_: Working directory for the emulator. If omitted, uses the executable's directory.
- **preview_dir** _(optional)_: Preview directory for game images.
 
> **Tip:**  
> On Windows, use `\` or `\\` for paths.  
> On Linux, use `/`.

---

## Keyboard Shortcuts

| Key      | Use                                         |
|----------|---------------------------------------------|
| Esc      | Close the program.                          |
| Tab      | Change between the left and right panel.    |
| Ctrl+A   | Show information/about dialog.              |
| Ctrl+R   | Reload information from config.ini.         |

---

## Notes for Cross-Platform Use

- **Launching Emulators:**  
  - On Windows, `jgemu` uses the shell to launch `.exe` files (so file associations, etc. work as expected).
  - On Linux, the command is executed directly; ensure your emulator is executable (`chmod +x`) and referenced with the full path if not in your `PATH`.
- **Icons:**  
  - Windows: Use `icon.ico` for the window icon.
  - Linux: Use `icon.png` (if present) for the window icon.
- **Paths:**  
  - All paths in `config.ini` are normalized, so you can use either `/` or `\` as appropriate for your OS.
- **Parameters:**  
  - Emulator parameters are comma-separated in `config.ini` and split automatically.

---

## Troubleshooting

- **Emulator doesn’t launch:**  
  - Check that all paths in `config.ini` are correct and point to actual files.
  - On Linux, ensure the emulator binary is executable.
  - On Windows, check that the `.exe` path is correct and the emulator runs from the command line.
- **No games listed:**  
  - Make sure the `games` directory exists and contains files with extensions listed in `extensions`.

---

## Contact

For questions, suggestions, or bug reports, contact:  
**gegecom83@gmail.com**

---

## License

MIT License
