# Every directory holding a herdr-plugin.toml is a plugin.
PLUGINS := $(patsubst %/,%,$(dir $(wildcard */herdr-plugin.toml)))
HERDR_CONFIG := $(HOME)/.config/herdr/config.toml

.PHONY: install
install: link config

.PHONY: link
link:
	@for p in $(PLUGINS); do \
		herdr plugin unlink $$p >/dev/null 2>&1; \
		herdr plugin link $(CURDIR)/$$p >/dev/null && echo "linked $$p"; \
	done

# herdr has no config includes, so the live config is config.toml plus each
# plugin's keys.toml, rebuilt on every install.
.PHONY: config
config:
	@tmp=$$(mktemp); cat config.toml > $$tmp; \
	for k in $(wildcard */keys.toml); do printf '\n' >> $$tmp; cat $$k >> $$tmp; done; \
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
