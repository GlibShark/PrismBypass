# PrismBypass

PrismBypass is a local tool for managing accounts in **PrismLauncher** on Windows.  
The project simplifies working with the `accounts.json` file and allows you to quickly restore or reset the state of accounts without manually editing configurations.

The tool is focused on convenience, transparency, and minimal system interference.

---

## Key features

- **Full account reset**
Creates a new `accounts.json` file with the basic MSA account configuration.

- **Add account**  
  Adds an MSA account to the existing list without duplication or file corruption.

- **Delete accounts.json file**  
  Allows you to completely clear PrismLauncher accounts.

- **Automatically restart PrismLauncher**  
  The launcher closes correctly before changes and restarts after they are applied.

- **Automatic update**  
  A separate loader checks for a new version via GitHub Releases, downloads it, and runs the current executable file.

---

## How it works

PrismBypass works exclusively locally:

1. Identifies the running process `prismlauncher.exe`
2. Correctly terminates it
3. Makes changes to the file:

%APPDATA%\PrismLauncher\accounts.json

4. Restart PrismLauncher

The tool does not use hidden methods to interact with the system and does not modify any other files.

---

## System requirements

- Windows 10 or newer
- PrismLauncher installed
- Python 3.9+ (to run from source code) or a ready-made `.exe` file

---

## Technologies used

- Python
- Tkinter + sv_ttk (graphical interface)
- psutil (process management)
- requests (updates via GitHub API)
- Nuitka (compilation into an executable file)

---

## Notes

The project is intended for educational, testing, and local purposes.  
The user is solely responsible for using the tool in accordance with the rules of the services with which it interacts.

---

## Contacts

- Telegram: **https://t.me/prismbypass**
