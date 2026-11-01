# Commands

## herdr-app

Prefix is `ctrl-a` (the `prefix` mod), and only the keys its menu shows work.

| Key | What it does |
| --- | --- |
| `r` | Rename the focused agent. |
| `b` | Block the focused agent: move it into its space's `⛔ blocked` tab, which the tab bar hides. It stays in the sidebar under ⛔ Blocked; click it to show it. On a blocked agent, `b` moves it back to the tab it came from. |
| `c` | Open the agent's folder in Cursor over WSL. |
| `v` / `x` | Split right / close pane, evening out widths after. |
| `=` | Even out pane widths. |
| `z` | Zoom or unzoom, lone panes too. |
| `s` / `R` | New space / rename space. |
| `⇧1` / `⇧2` | Theme `grey` / `rm-dev`. |
| `:` / `?` | Palette / help. |

## Terminal herdr

Prefix is `ctrl+a`, and the keys are the herdr-app menu above and nothing else: every other built-in binding is unset in `config.toml`. Plugin keys live in each plugin's `keys.toml`; any action also runs with `herdr plugin action invoke <action> --plugin <plugin>`.

| Key | Source | What it does |
| --- | --- | --- |
| `r` | built-in `rename_pane` | Rename the focused pane; the name shows on its border and in the sidebar. |
| `b` | `herdr-blocked.toggle` | Move the focused pane into its workspace's `⛔ blocked` tab, or back to its original tab. It stays in the agents list, tagged `⛔ blocked`. |
| `c` | `herdr-app-parity.cursor` | Open the pane's folder in Cursor. |
| `v` / `x` | `herdr-app-parity.split` / `close` | Split right / close pane, evening out widths after. |
| `z` | built-in `zoom` | Zoom. |
| `=` | `herdr-app-parity.even` | Even out the panes in the tab. |
| `s` / `R` | built-in | New workspace / rename workspace. |
| `⇧1` / `⇧2` | `herdr-app-parity.theme-*` | Theme `grey` / `rm-dev`, written into the live config until the next `make config`. |
| `:` / `?` | built-in `goto` / `help` | Session navigator / keybinding help. |
