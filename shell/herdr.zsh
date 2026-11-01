# herdr-app (Windows) can't see WSL folders: label this terminal with its cwd so
# herdr-app mods (and Claude's status line) can find the repo. Needs WSLENV=HC_TERMINAL_ID.
if [[ -n $HC_TERMINAL_ID ]]; then
  local_hc=(/mnt/c/Users/*/AppData/Local/Programs/herdr-core/hc.exe(N[1]))
  export HERDR_HC=${local_hc[1]}
  unset local_hc
  if [[ -n $HERDR_HC ]]; then
    _herdr_cwd() { ("$HERDR_HC" label "$HC_TERMINAL_ID" "cwd=$PWD" >/dev/null 2>&1 &) }
    autoload -Uz add-zsh-hook && add-zsh-hook chpwd _herdr_cwd && _herdr_cwd
  fi
fi
