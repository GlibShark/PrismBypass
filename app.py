import json
import os
import psutil
import subprocess
import threading
import tkinter as tk
from tkinter import ttk
import sv_ttk
import ctypes
import sys


try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

PRISM_EXE = "prismlauncher.exe"
NEW_ACCOUNT = {
    "entitlement": {
        "canPlayMinecraft": True,
        "ownsMinecraft": True
    },
    "type": "MSA"
}

ACCOUNTS_PATH = os.path.join(
    os.getenv("APPDATA"),
    "PrismLauncher",
    "accounts.json"
)

# ===== PrismLauncher Functions =====
def find_prism():
    for p in psutil.process_iter(["name"]):
        try:
            if p.info["name"] and p.info["name"].lower() == PRISM_EXE.lower():
                return p
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None


def close_prism():
    proc = find_prism()
    if not proc:
        return None
    path = proc.exe()
    proc.terminate()
    proc.wait()
    return path


def _run_prism_silent(path):
    try:
        subprocess.Popen(
            [path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except Exception:
        pass


def open_prism(path):
    if path:
        threading.Thread(
            target=_run_prism_silent,
            args=(path,),
            daemon=True
        ).start()


def load_accounts():
    if not os.path.exists(ACCOUNTS_PATH):
        return {"accounts": [], "formatVersion": 3}
    with open(ACCOUNTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_accounts(data):
    os.makedirs(os.path.dirname(ACCOUNTS_PATH), exist_ok=True)
    with open(ACCOUNTS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def delete_accounts_file():
    if os.path.exists(ACCOUNTS_PATH):
        os.remove(ACCOUNTS_PATH)


def add_account(data):
    for acc in data.get("accounts", []):
        if acc.get("type") == "MSA" and acc.get("entitlement") == NEW_ACCOUNT["entitlement"]:
            return data
    data.setdefault("accounts", []).append(NEW_ACCOUNT)
    return data


def full_replace():
    return {
        "accounts": [NEW_ACCOUNT],
        "formatVersion": 3
    }

# ===== Tkinter Actions =====
def action_full_replace():
    path = close_prism()
    save_accounts(full_replace())
    open_prism(path)


def action_add_account():
    path = close_prism()
    data = load_accounts()
    save_accounts(add_account(data))
    open_prism(path)


def action_delete_accounts():
    path = close_prism()
    delete_accounts_file()
    open_prism(path)

root = tk.Tk()
def resource_path(rel):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel)
    return os.path.join(os.path.dirname(__file__), rel)

try:
    root.iconbitmap(resource_path("icon.ico"))
except Exception:
    pass


root.title("t.me/prismbypass")
root.geometry("400x200")
root.resizable(False, False)

sv_ttk.set_theme("dark")

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12))

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Button(
    frame,
    text="Full account reset",
    command=action_full_replace
).pack(fill=tk.X, pady=5)

ttk.Button(
    frame,
    text="Add account",
    command=action_add_account
).pack(fill=tk.X, pady=5)

ttk.Button(
    frame,
    text="Delete accounts.json",
    command=action_delete_accounts
).pack(fill=tk.X, pady=5)

ttk.Button(
    frame,
    text="Exit",
    command=root.destroy
).pack(fill=tk.X, pady=5)

root.mainloop()
