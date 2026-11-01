"""Actions that match herdr-app's ctrl-a menu: split and close with even widths, even out, open in Cursor, pick a theme."""
import glob
import json
import os
import re
import socket
import subprocess
import sys

HERDR = os.environ.get("HERDR_BIN_PATH", "herdr")
CONFIG = os.path.expanduser("~/.config/herdr/config.toml")
HERE = os.path.dirname(os.path.abspath(__file__))


def rpc(method, params):
    with socket.socket(socket.AF_UNIX) as s:
        s.connect(os.environ["HERDR_SOCKET_PATH"])
        s.sendall(json.dumps({"id": "1", "method": method, "params": params}).encode() + b"\n")
        return json.loads(s.makefile().readline())


def snapshot():
    out = subprocess.run([HERDR, "api", "snapshot"], capture_output=True, text=True).stdout
    return json.loads(out)["result"]["snapshot"]


def focused(snap):
    # Actions run outside any pane, so use the UI-focused one.
    return next((p for p in snap["panes"] if p["pane_id"] == snap.get("focused_pane_id")), None)


def weight(node, direction):
    if node["type"] != "split" or node["direction"] != direction:
        return 1
    return weight(node["first"], direction) + weight(node["second"], direction)


def ratios(node, path=()):
    """Splits each run of same-direction splits so every pane in it gets an equal share."""
    if node["type"] != "split":
        return []
    a, b = weight(node["first"], node["direction"]), weight(node["second"], node["direction"])
    return [(list(path), a / (a + b))] + ratios(node["first"], path + (False,)) + ratios(node["second"], path + (True,))


def even(tab=None):
    if not tab:
        pane = focused(snapshot())
        if not pane:
            return
        tab = pane["tab_id"]
    layout = rpc("layout.export", {"tab_id": tab}).get("result")
    if not layout:  # the tab closed with its last pane
        return
    root = layout["layout"]["root"]
    for path, ratio in ratios(root):
        rpc("layout.set_split_ratio", {"tab_id": tab, "path": path, "ratio": ratio})


def split():
    pane = focused(snapshot())
    if pane:
        cwd = ["--cwd", pane["cwd"]] if pane.get("cwd") else []
        subprocess.run([HERDR, "pane", "split", pane["pane_id"], "--direction", "right", "--focus", *cwd], capture_output=True)
        even(pane["tab_id"])


def close():
    pane = focused(snapshot())
    if pane:
        subprocess.run([HERDR, "pane", "close", pane["pane_id"]], capture_output=True)
        even(pane["tab_id"])


def cursor():
    snap = snapshot()
    pane = focused(snap)
    if not pane:
        return
    if pane.get("cwd"):
        # Plugin actions get no shell PATH or aliases, so find Cursor's WSL launcher directly.
        launcher = next(iter(glob.glob("/mnt/c/Users/*/AppData/Local/Programs/cursor/resources/app/bin/cursor")), None)
        if launcher:
            subprocess.Popen([launcher, "--new-window", pane["cwd"]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def theme(name):
    with open(os.path.join(HERE, "themes", f"{name}.toml")) as f:
        block = f.read().strip()
    with open(CONFIG) as f:
        text = f.read()
    text = re.sub(r"(?ms)^\[theme(\.custom)?\]\n.*?(?=^\[|\Z)", "", text).rstrip() + "\n\n" + block + "\n"
    with open(CONFIG, "w") as f:
        f.write(text)
    subprocess.run([HERDR, "server", "reload-config"], capture_output=True)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "even":
        even()
    elif cmd == "split":
        split()
    elif cmd == "close":
        close()
    elif cmd == "cursor":
        cursor()
    elif cmd == "theme":
        theme(sys.argv[2])
