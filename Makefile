PLUGINS := $(patsubst %/,%,$(dir $(wildcard */herdr-plugin.toml)))
HERDR_CONFIG := $(HOME)/.config/herdr/config.toml
# herdr-app-parity's ⇧1/⇧2 swap the theme in the live config until the next make config.
THEME ?= rm-dev

# herdr-app and herdr-core run on Windows; their config lives in the Windows profile.
WIN_HOME ?= $(patsubst %/.config/herdr-app,%,$(firstword $(wildcard /mnt/c/Users/*/.config/herdr-app)))
APP_HOME := $(WIN_HOME)/.config/herdr-app
CORE_HOME := $(WIN_HOME)/AppData/Roaming/herdr-core

.PHONY: install
install: link config install-app

# Copied, not linked: Windows can't follow WSL symlinks. herdr-app reloads these live.
.PHONY: install-app
install-app:
	@[ -d "$(APP_HOME)" ] || { echo "no herdr-app config found; set WIN_HOME"; exit 1; }
	@cp -r app/. $(APP_HOME)/ && echo "installed $(APP_HOME)"
	@mkdir -p $(CORE_HOME) && cp core/config.toml $(CORE_HOME)/config.toml && echo "installed $(CORE_HOME)/config.toml"

.PHONY: link
link:
	@for p in $(PLUGINS); do \
		herdr plugin unlink $$p >/dev/null 2>&1; \
		herdr plugin link $(CURDIR)/$$p >/dev/null && echo "linked $$p"; \
	done

# herdr has no config includes, so the live config is config.toml plus each
# plugin's keys.toml and the THEME file, rebuilt on every install.
.PHONY: config
config:
	@tmp=$$(mktemp); cat config.toml > $$tmp; \
	for k in $(wildcard */keys.toml); do printf '\n' >> $$tmp; cat $$k >> $$tmp; done; \
	printf '\n' >> $$tmp; cat herdr-app-parity/themes/$(THEME).toml >> $$tmp; \
	if cmp -s $$tmp $(HERDR_CONFIG); then rm $$tmp; echo "config unchanged"; else \
		mkdir -p $(dir $(HERDR_CONFIG)); \
		[ -f $(HERDR_CONFIG) ] && cp $(HERDR_CONFIG) $(HERDR_CONFIG).bak-$$(date +%Y%m%d-%H%M%S); \
		mv $$tmp $(HERDR_CONFIG) && echo "installed $(HERDR_CONFIG)"; \
		herdr server reload-config >/dev/null 2>&1 || true; \
	fi

.PHONY: uninstall
uninstall:
	@for p in $(PLUGINS); do herdr plugin unlink $$p >/dev/null 2>&1 && echo "unlinked $$p"; done

.PHONY: list
list:
	@herdr plugin list
