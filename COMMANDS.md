# Commands

Prefix is `ctrl+a`. Keybindings are set in herdr's `config.toml` (source: `claude-code-config/herdr/config.toml`). Every action can also be run with `herdr plugin action invoke <action> --plugin <plugin>`.

| Plugin | Action | Keybinding | What it does |
| --- | --- | --- | --- |
| `herdr-blocked` | `toggle` | `prefix+shift+b` | Move the focused pane into its workspace's `⛔ blocked` tab, or back to its original tab if it is already there. |
| `herdr-blocked` | `show` | `prefix+alt+b` | Show or hide blocked agents in the sidebar agents list. |
