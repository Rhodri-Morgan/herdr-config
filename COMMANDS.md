# Commands

## herdr-app

Prefix is `ctrl-a` (the `prefix` mod).

| Key | What it does |
| --- | --- |
| `r` | Rename the focused agent. |
| `b` | Block the focused agent: move it into its space's `⛔ blocked` tab, which the tab bar hides. It stays in the sidebar under ⛔ Blocked; click it to show it. On a blocked agent, `b` moves it back to the tab it came from. |
| `e` / `E` | Open the agent's folder, or every agent's folder in the space, in Cursor over WSL. |
| `v` / `x` / `=` | Split right / close pane, evening out widths / even out. |
| `z` | Zoom or unzoom, lone panes too. |
| `S` / `R` | New space / rename space. |
| `T` | Rename tab. |
| `c` / `t` | New tab. |
| `n` / `p` / `&` | Next tab / previous tab / close tab. |
| `1`–`9` | Select tab. |
| `h` `j` `k` `l` or arrows | Focus pane left / down / up / right. |
| `H` `J` `K` `L` | Swap pane left / down / up / right. |
| `(` / `)` | Previous / next space. |
| `⇧1` / `⇧2` | Theme `grey` / `rm-dev`. |
| `:` / `?` | Palette / help. |

## Terminal herdr

Prefix is `ctrl+a`. Each plugin's keybindings live in its `keys.toml`. Every action can also be run with `herdr plugin action invoke <action> --plugin <plugin>`.

| Plugin | Action | Keybinding | What it does |
| --- | --- | --- | --- |
| `herdr-blocked` | `toggle` | `prefix+shift+b` | Move the focused pane into its workspace's `⛔ blocked` tab, or back to its original tab if it is already there. |
| `herdr-blocked` | `show` | `prefix+alt+b` | Show or hide blocked agents in the sidebar agents list. |
