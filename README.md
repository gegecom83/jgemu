# jgemu.py
jgemu is a simple emulator launcher written in PyQt5. It's a portable and convenient menu to run all your games from a single place.
Its creation was inspired by [Yava](https://github.com/Beluki/Yava).

## Keyboard shortcuts
| Key    | Use                                              |
| ------ | ------------------------------------------------ |
| Esc    | Close the program.                               |
| Tab    | Change between the left and right panel.         |
| Ctrl+A | Show an information message.                     |
| Ctrl+R | Reload information config.ini.                   |

## Configuration
jgemu is configured using a file named "config.ini". This file contains everything jgemu needs to know about the folders
and files it will launch.

Here is an example:
```ini
[Game Boy]
games      = C:\Games\Game Boy\
executable = C:\Emulators\BGB\bgb.exe
extensions = .zip, .gb

# [NEC PC Engine CD]
# games       = D:\NEC PC Engine CD\
# executable  = C:\Emulators\RetroArch\retroarch.exe
# extensions  = .cue
# parameters  = -L cores\mednafen_pce_libretro.dll
# working_dir = C:\Emulators\RetroArch\
```

