"""Park blocked tasks: move the pane into a "⛔ blocked" tab, tag it, and hide it from the agents list.

A pane is blocked exactly when it sits in its workspace's blocked tab. The state
file remembers each blocked pane's original tab (so unblocking can put it back)
and the show/hide flag, since herdr does not report the active agent view.
"""
import json
import os
import socket
import subprocess
import sys

SOURCE = "herdr-blocked"
TAG = "⛔ blocked"
HERDR = os.environ.get("HERDR_BIN_PATH", "herdr")


def herdr(*args):
    out = subprocess.run([HERDR, *args], capture_output=True, text=True)
    return json.loads(out.stdout) if out.stdout.strip() else {}


def rpc(method, params):
    # agent.view.set has no CLI wrapper, so talk to the socket directly.
    with socket.socket(socket.AF_UNIX) as s:
        s.connect(os.environ["HERDR_SOCKET_PATH"])
        s.sendall(json.dumps({"id": "1", "method": method, "params": params}).encode() + b"\n")
        return json.loads(s.makefile().readline())


def notify(msg):
    herdr("notification", "show", "Blocked", "--body", msg)


def snapshot():
    return herdr("api", "snapshot")["result"]["snapshot"]


def state_path():
    d = subprocess.run([HERDR, "plugin", "config-dir", SOURCE], capture_output=True, text=True).stdout.strip()
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, "state.json")


def load():
    try:
        with open(state_path()) as f:
            return {"show": False, "origin": {}, **json.load(f)}
    except (OSError, ValueError):
        return {"show": False, "origin": {}}


def save(state):
    with open(state_path(), "w") as f:
        json.dump(state, f)


def apply_view(state):
    if state["show"]:
        return rpc("agent.view.clear", {"source": SOURCE})
    blocked = {"op": "eq", "field": {"token": "blocked"}, "value": TAG}
    rpc("agent.view.set", {"source": SOURCE, "label": "hiding blocked", "filter": {"op": "not", "filter": blocked}})


def blocked_tab(snap, ws):
    return next((t for t in snap["tabs"] if t["workspace_id"] == ws and t["label"] == TAG), None)


def block(snap, pane, state):
    ws = pane["workspace_id"]
    tab = blocked_tab(snap, ws)
    if tab:
        herdr("pane", "move", pane["pane_id"], "--tab", tab["tab_id"], "--split", "down", "--no-focus")
    else:
        created = herdr("tab", "create", "--workspace", ws, "--label", TAG, "--no-focus")["result"]
        herdr("pane", "move", pane["pane_id"], "--tab", created["tab"]["tab_id"], "--split", "right", "--no-focus")
        herdr("pane", "close", created["root_pane"]["pane_id"])  # placeholder shell from tab create
    herdr("pane", "report-metadata", pane["pane_id"], "--source", SOURCE, "--token", f"blocked={TAG}")
    state["origin"][pane["pane_id"]] = pane["tab_id"]
    notify(f"Blocked {pane['pane_id']}")


def unblock(snap, pane, state):
    ws = pane["workspace_id"]
    tabs = [t["tab_id"] for t in snap["tabs"] if t["workspace_id"] == ws and t["label"] != TAG]
    origin = state["origin"].pop(pane["pane_id"], None)
    if origin in tabs:
        herdr("pane", "move", pane["pane_id"], "--tab", origin, "--split", "right", "--focus")
    elif tabs:
        herdr("pane", "move", pane["pane_id"], "--tab", tabs[0], "--split", "right", "--focus")
    else:
        herdr("tab", "rename", pane["tab_id"], "1")  # only tab left: just make it a normal tab
    herdr("pane", "report-metadata", pane["pane_id"], "--source", SOURCE, "--clear-token", "blocked")
    notify(f"Unblocked {pane['pane_id']}")


def toggle(state):
    snap = snapshot()
    # Action runs outside any pane, so use the UI-focused pane.
    pane = next((p for p in snap["panes"] if p["pane_id"] == snap.get("focused_pane_id")), None)
    if not pane:
        return notify("No focused pane")
    tab = blocked_tab(snap, pane["workspace_id"])
    (unblock if tab and tab["tab_id"] == pane["tab_id"] else block)(snap, pane, state)

    ws = pane["workspace_id"]
    flag = ["--token", f"blocked={TAG}"] if blocked_tab(snapshot(), ws) else ["--clear-token", "blocked"]
    herdr("workspace", "report-metadata", ws, "--source", SOURCE, *flag)


def main():
    state = load()
    if sys.argv[1] == "toggle":
        toggle(state)
    elif sys.argv[1] == "show":
        state["show"] = not state["show"]
        notify("Showing blocked tasks" if state["show"] else "Hiding blocked tasks")
    save(state)
    apply_view(state)


if __name__ == "__main__":
    main()
