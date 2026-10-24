# herdr-plugins

My herdr plugins. Each directory with a `herdr-plugin.toml` is one plugin.

| Plugin | What it does |
| --- | --- |
| `herdr-blocked` | Parks the focused pane in a `⛔ blocked` tab, tags it, and hides it from the agents list. |
| `herdr-open-pr` | Opens the GitHub PR for the focused pane's branch. |

## Install

```sh
make install    # link every plugin into herdr (safe to re-run)
make uninstall  # unlink them
make list       # show installed plugins
```

Plugins are linked, not copied, so edits here take effect on the next action run.

Keybindings live in herdr's `config.toml` (kept in `claude-code-config/herdr/config.toml`).

## Adding a plugin

Create `<name>/herdr-plugin.toml` with `id = "<name>"`, then `make install`.
