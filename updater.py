import requests
import os
import sys
import subprocess
import time
import tempfile

# ================= CONFIG =================
REPO = "GlibShark/PrismBypass"
EXE_NAME = "prismbypass.exe"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"

TEMP_DIR = os.path.join(tempfile.gettempdir(), "PrismBypass")
EXE_PATH = os.path.join(TEMP_DIR, EXE_NAME)
VERSION_FILE = os.path.join(TEMP_DIR, "version.txt")

# ================= BANNER =================
ASCII_ART = r"""
       .__                  __                    .___       __                
  _____|  |__ _____ _______|  | ____ ________   __| _/____ _/  |_  ___________ 
 /  ___/  |  \\__  \\_  __ \  |/ /  |  \____ \ / __ |\__  \\   __\/ __ \_  __ \
 \___ \|   Y  \/ __ \|  | \/    <|  |  /  |_> > /_/ | / __ \|  | \  ___/|  | \/
/____  >___|  (____  /__|  |__|_ \____/|   __/\____ |(____  /__|  \___  >__|   
     \/     \/     \/           \/     |__|        \/     \/          \/             
"""

# ================= UTILS =================
def print_banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(ASCII_ART)
    print("PrismBypass Loader")
    print("Auto-updating to the latest version\n")
    time.sleep(1)


def get_latest_release():
    print("[*] Checking latest GitHub release...")
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    return r.json()


def download_file(url, path):
    print("[*] Downloading latest executable...")
    with requests.get(url, stream=True, timeout=30) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def get_local_version():
    if not os.path.exists(VERSION_FILE):
        return None
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def save_local_version(version):
    with open(VERSION_FILE, "w", encoding="utf-8") as f:
        f.write(version)

# ================= MAIN LOGIC =================
def update_and_run():
    print_banner()
    os.makedirs(TEMP_DIR, exist_ok=True)

    try:
        release = get_latest_release()
    except Exception as e:
        print(f"[!] Failed to fetch release info: {e}")
        time.sleep(3)
        os._exit(1)

    latest_version = release.get("tag_name", "unknown")
    local_version = get_local_version()

    print(f"[*] Latest version: {latest_version}")
    print(f"[*] Local version : {local_version or 'none'}")

    assets = release.get("assets", [])
    exe_asset = next(
        (a for a in assets if a["name"].lower() == EXE_NAME.lower()),
        None
    )

    if not exe_asset:
        print("[!] prismbypass.exe not found in release assets")
        time.sleep(3)
        os._exit(1)

    if local_version != latest_version or not os.path.exists(EXE_PATH):
        temp_download = EXE_PATH + ".new"

        try:
            download_file(exe_asset["browser_download_url"], temp_download)
        except Exception as e:
            print(f"[!] Download failed: {e}")
            time.sleep(3)
            os._exit(1)

        if os.path.exists(EXE_PATH):
            try:
                os.remove(EXE_PATH)
            except Exception:
                pass

        os.rename(temp_download, EXE_PATH)
        save_local_version(latest_version)
        print("[✓] Updated successfully")
    else:
        print("[✓] Already up to date")

    print("[*] Launching PrismBypass...\n")

    subprocess.Popen(
        [EXE_PATH],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
        close_fds=True
    )

    os._exit(0)

# ================= ENTRY =================
if __name__ == "__main__":
    update_and_run()
