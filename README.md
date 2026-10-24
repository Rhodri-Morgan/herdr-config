# herdr-plugins

My herdr plugins. Each directory with a `herdr-plugin.toml` is one plugin.

| Plugin | What it does |
| --- | --- |
| `herdr-blocked` | Parks the focused pane in a `⛔ blocked` tab, tags it in the sidebar, and hides it from the agents list. |

Keybindings and actions: [COMMANDS.md](COMMANDS.md).

## Install

```sh
make install    # link every plugin and install herdr's config.toml (safe to re-run)
make link       # link plugins only
make config     # install config only
make uninstall  # unlink plugins
make list       # show installed plugins
```

Plugins are linked, not copied, so edits here take effect on the next action run.

## Config

This repo owns herdr's `~/.config/herdr/config.toml`. `make config` builds it from `config.toml` plus every plugin's `keys.toml`, backs up the old file if it changed, and reloads herdr. Edit those files here, not the live config, which is overwritten on install.

## Requirements

- herdr 0.9.0+
- `python3` for `herdr-blocked`
