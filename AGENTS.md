# AGENTS.md

herdr plugins, one per top-level directory. A directory is a plugin when it holds a `herdr-plugin.toml`; the `Makefile` discovers plugins that way.

## Layout

- `<plugin>/herdr-plugin.toml`: manifest. `id` must equal the directory name, since `make install` unlinks by directory name.
- `<plugin>/<script>`: what each `[[actions]]` `command` runs, relative to the plugin directory.
- `<plugin>/keys.toml`: optional `[[keys.command]]` entries binding the plugin's actions.
- `config.toml`: base herdr config, without plugin keybindings.
- `COMMANDS.md`: one row per action. Update it whenever an action or keybinding changes.

## Writing actions

- Actions run outside any pane, so target the UI-focused pane (`herdr pane current` or `focused_pane_id` from `herdr api snapshot`), never `--current`.
- Call herdr through `${HERDR_BIN_PATH:-herdr}`. Socket calls with no CLI wrapper (for example `agent.view.set`) go to `$HERDR_SOCKET_PATH` as newline-delimited JSON.
- Report failures with `herdr notification show`; action stdout is only visible in `herdr plugin log list`.
- Run `herdr --help`, `herdr <group>` and `herdr api schema --json` to check the CLI and API; the installed binary is the authority.
- Keep plugin state in `herdr plugin config-dir <id>`, not in this repo.

## Testing

Test against a throwaway session, not the live one: run `herdr --session <name>` in a split pane, then point commands at it with `HERDR_SOCKET_PATH=~/.config/herdr/sessions/<name>/herdr.sock herdr --session <name> ...`. `herdr pane read <pane> --source visible` shows the rendered sidebar. Stop it with `herdr --session <name> server stop`.

## Config

`make config` replaces the live `~/.config/herdr/config.toml` with `config.toml` followed by every `*/keys.toml`; herdr has no config includes, so this concatenation is the only way to compose it. Put a plugin's bindings in its `keys.toml` and everything else in `config.toml`. Run `herdr server reload-config` and check `diagnostics` is empty after changing either.
