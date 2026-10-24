# herdr-plugins

My herdr plugins. Each directory with a `herdr-plugin.toml` is one plugin.

| Plugin | What it does |
| --- | --- |
| `herdr-blocked` | Parks the focused pane in a `⛔ blocked` tab, tags it in the sidebar, and hides it from the agents list. |
| `herdr-open-pr` | Opens the GitHub PR for the focused pane's branch. |

Keybindings and actions: [COMMANDS.md](COMMANDS.md).

## Install

```sh
make install    # link every plugin into herdr (safe to re-run)
make uninstall  # unlink them
make list       # show installed plugins
```

Plugins are linked, not copied, so edits here take effect on the next action run.

## Requirements

- herdr 0.9.0+ (`herdr-blocked`), 0.7.0+ (`herdr-open-pr`)
- `python3` for `herdr-blocked`
- `jq` and `gh` for `herdr-open-pr`
