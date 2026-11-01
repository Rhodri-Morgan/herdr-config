// tmux-style prefix: ctrl-a (keys.json: "mod.open:prefix") opens this,
// the next key runs a command from KEYS and closes it. Esc cancels.

import { View, div } from "gpui-kit";
import { v_flex, h_flex, InputState, Input } from "gpui-base";
import { run, props, closeOverlay, theme, commands, focused, terminals, hc, panes, shared, setShared, spaces, exec as sh } from "herdr";

const KEYS = {
  c: "tab.new",
  n: "tab.next",
  p: "tab.prev",
  T: "tab.rename",
  "&": "tab.close",
  v: "pane.split:right",
  "=": "pane.even",
  t: "tab.new",
  x: "pane.close",
  z: "pane.zoom",
  h: "pane.go:left",
  j: "pane.go:down",
  k: "pane.go:up",
  l: "pane.go:right",
  left: "pane.go:left",
  down: "pane.go:down",
  up: "pane.go:up",
  right: "pane.go:right",
  H: "pane.swap:left",
  J: "pane.swap:down",
  K: "pane.swap:up",
  L: "pane.swap:right",
  S: "space.new",
  R: "space.rename",
  r: "agent.rename",
  e: "cursor.agent",
  E: "cursor.space",
  "(": "space.prev",
  ")": "space.next",
  b: "blocked.toggle",
  ":": "app.palette",
  "?": "app.help",
  ...Object.fromEntries([1, 2, 3, 4, 5, 6, 7, 8, 9].map((n) => [String(n), `tab.select:${n}`])),
};

// ponytail: weight 1 on every pane in the tab; evens a row of right splits, not nested down splits.
function even() {
  const tab = focused()?.tab;
  for (const p of panes()) if (p.tab === tab) run("layout.resize", { id: p.pane, weight: 1 });
}

// Herdr won't zoom a tab's only pane, so a lone pane gets a "solo" zoom the
// agents list and pane header honor instead (shared "zoom.solo" = pane id).
function zoom() {
  const f = focused();
  const lone = panes().filter((p) => p.tab === f?.tab).length === 1;
  if (shared("zoom.solo") === f?.pane || lone) setShared("zoom.solo", shared("zoom.solo") === f?.pane ? null : f?.pane);
  else run("pane.zoom", {});
}

const CURSOR = "%LOCALAPPDATA%\\Programs\\cursor\\resources\\app\\bin\\cursor.cmd";

// Folders come from the cwd label the zsh hook and Claude status line set.
function cursor(all) {
  const me = focused()?.terminal, space = spaces().find((s) => s.active)?.id;
  const dirs = new Set(terminals()
    .filter((x) => (all ? x.labels?.["herdr.space"] === space : x.address === me))
    .map((x) => x.labels?.cwd).filter(Boolean));
  if (dirs.size) sh("cmd.exe", ["/c", CURSOR, "--new-window", ...[...dirs].flatMap((d) => ["--folder-uri", `vscode-remote://wsl+Ubuntu${d}`])]);
}

const THEMES = ["grey", "rm-dev"];
// Windows reports shift+digit as the symbol it types, which differs by keyboard (UK " vs US @).
const SHIFTED = { "!": 1, "@": 2, '"': 2 };

// Blocking takes several steps with focus moving between tabs, which closes this
// overlay, so the agents-named mod (always on screen) runs it from this request.
function requestBlock() {
  const f = focused();
  if (f?.terminal) setShared("blocked.req", { term: f.terminal, tab: f.tab, space: spaces().find((s) => s.active)?.id, at: Date.now() });
}

function exec(action) {
  const [name, value] = action.split(/:(.*)/);
  if (value === undefined) return run(name, {});
  const first = commands().find((c) => c.name === name)?.args[0]?.name;
  run(name, { [first]: value });
}

export default class Prefix extends View {
  init(_props, cx) {
    this.terminal = focused()?.terminal;
    this.handle = cx.focus_handle();
    this.handle.focus();
  }

  // Agent names are hc labels, so they outlive the app; the agents-named mod shows them.
  rename(cx) {
    const current = terminals().find((x) => x.address === this.terminal)?.labels?.name ?? "";
    this.input = InputState.new({ value: current });
    this.input.on("submit", () => {
      hc(["label", this.terminal, `name=${this.input.value().trim()}`]);
      closeOverlay(props().overlay);
    });
    this.input.focus();
    cx.notify();
  }

  render(cx) {
    const t = theme();
    const shown = [
      ["Agent", [["r", "rename"], ["b", "block / unblock"], ["e", "open in Cursor"], ["E", "space in Cursor"]]],
      ["Pane", [["v", "split right"], ["=", "even out"], ["x", "close"], ["z", "zoom"]]],
      ["Space", [["S", "new"], ["R", "rename"]]],
      ["App", [[":", "palette"], ["?", "help"]]],
      ["Theme \u21e7", THEMES.map((name, i) => [String(i + 1), name])],
    ];
    return v_flex()
      .id("prefix")
      .track_focus(this.handle)
      .on_key_down((e, cx) => {
        if (["shift", "control", "alt", "platform"].includes(e.key)) return;
        if (this.input) {
          if (e.key === "escape") closeOverlay(props().overlay);
          return;
        }
        cx.stop_propagation();
        const n = SHIFTED[e.key_char ?? e.key] ?? SHIFTED[e.key] ?? (e.modifiers.shift ? Number(e.key) : 0);
        if (n >= 1 && n <= THEMES.length) {
          const name = THEMES[n - 1];
          if (name) run("app.theme", { name });
          return closeOverlay(props().overlay);
        }
        const action = KEYS[e.key_char ?? e.key] ?? KEYS[e.key];
        if (action === "blocked.toggle") return (requestBlock(), closeOverlay(props().overlay));
        if (action === "agent.rename" && this.terminal) return this.rename(cx);
        if (action?.startsWith("cursor.")) return (cursor(action === "cursor.space"), closeOverlay(props().overlay));
        if (action === "pane.zoom") return (zoom(), closeOverlay(props().overlay));
        if (action === "pane.even") return (even(), closeOverlay(props().overlay));
        if (action === "pane.split:right" || action === "pane.close") {
          exec(action);
          // The change reaches panes() a moment after the command.
          return cx.timer.after(150, () => (even(), closeOverlay(props().overlay)));
        }
        closeOverlay(props().overlay);
        if (action && !e.modifiers.control && !e.modifiers.alt) exec(action);
      })
      .size_full()
      .p(14)
      .bg(t.popover)
      .text_size(12)
      .when(Boolean(this.input), (el) => el.gap(8)
        .child(div().text_color(t.muted).child("Agent name (empty clears)"))
        .child(Input.new(this.input).h(32).px(10).rounded(8).border_1().border_color(t.accent).bg(t.background).text_color(t.foreground)))
      .when(!this.input, (el) => el.child(
        h_flex().gap(20).items_start().children(
          shown.map(([title, keys]) => v_flex().gap(4)
            .child(div().text_size(11).font_medium().text_color(t.dim).child(title))
            .children(keys.map(([k, what]) => h_flex().gap(8).child(div().w(14).text_color(t.accent).child(k)).child(div().text_color(t.muted).child(what))))),
        ),
      ));
  }
}
