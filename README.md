# herdr-config

My herdr setup: the herdr-app desktop config (Windows, driving WSL) and the terminal herdr plugins.

| Path | What it is |
| --- | --- |
| `app/` | herdr-app config: `keys.json`, `settings.json`, the `mine` layout, the `grey` and `rm-dev` themes, and mods. |
| `core/config.toml` | herdr-core config: terminals start in WSL Ubuntu. |
| `shell/herdr.zsh` | Sourced from `~/.zshrc`: labels each herdr terminal with its WSL folder. |
| `herdr-blocked/`, `herdr-app-parity/`, `config.toml` | Terminal herdr plugins and config, with the same ctrl-a keys as herdr-app. |

herdr-app mods:

| Mod | What it does |
| --- | --- |
| `prefix` | `ctrl-a` prefix menu: rename agent, block/unblock, Cursor, split/even/zoom, themes. |
| `agents-named` | Sidebar agents list: agent name over space name, grouped by space, blocked agents in their own group, zoom lock. |
| `pane-z` | Pane header: agent name, WSL path, zoom badge. |
| `tabs-bar` | Top bar: tab pills only when a space has more than one tab. |
| `chrome-rm` | Sidebar header with the rhodrimorgan.dev logo. |
| `spaces-rm`, `menu-rm` | Spaces list and right-click menu; Close on a space or tab skips the confirm. |

| Plugin | What it does |
| --- | --- |
| `herdr-blocked` | Parks the focused pane in a `⛔ blocked` tab and tags it in the agents list. |
| `herdr-app-parity` | herdr-app's menu actions herdr lacks: even out panes, open in Cursor, switch theme. |

Keybindings and actions: [COMMANDS.md](COMMANDS.md).

## Install

```sh
make install      # everything below (safe to re-run)
make install-app  # copy app/ and core/ into the Windows profile
make link         # link plugins only
make config       # install config only
make uninstall    # unlink plugins
make list         # show installed plugins
```

Plugins are linked, not copied, so edits here take effect on the next action run.

## Config

This repo owns herdr's `~/.config/herdr/config.toml`. `make config` builds it from `config.toml` plus every plugin's `keys.toml`, backs up the old file if it changed, and reloads herdr. Edit those files here, not the live config, which is overwritten on install.

## herdr-app

`make install-app` copies `app/` over `%USERPROFILE%\.config\herdr-app` and `core/config.toml` to `%APPDATA%\herdr-core`. They're copied, not linked, because Windows can't follow WSL symlinks, so edit here and re-run it.

Agents' WSL folders reach herdr-app through an `hc` label. Run `setx WSLENV HC_TERMINAL_ID` once in Windows and add `source ~/REPOS/herdr-config/shell/herdr.zsh` to `~/.zshrc`.

## Requirements

- herdr 0.9.0+
- `python3` for the plugins
