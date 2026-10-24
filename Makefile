# Every directory holding a herdr-plugin.toml is a plugin.
PLUGINS := $(patsubst %/,%,$(dir $(wildcard */herdr-plugin.toml)))

.PHONY: install
install:
	@for p in $(PLUGINS); do \
		herdr plugin unlink $$p >/dev/null 2>&1; \
		herdr plugin link $(CURDIR)/$$p >/dev/null && echo "linked $$p"; \
	done

.PHONY: uninstall
uninstall:
	@for p in $(PLUGINS); do herdr plugin unlink $$p >/dev/null 2>&1 && echo "unlinked $$p"; done

.PHONY: list
list:
	@herdr plugin list
