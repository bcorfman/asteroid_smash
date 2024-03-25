SHELL := env PYTHON_VERSION=$(PYTHON_VERSION) /bin/bash
.SILENT: devinstall install test lint format
PYTHON_VERSION ?= 3.12

prereq:
	sudo apt-get -y update
	sudo apt-get -y install libsdl1.2-dev
	sudo apt purge -y acpid acpi-support modemmanager whoopsie
	sudo apt-mark hold acpid acpi-support modemmanager whoopsie
	sudo apt-get -y install ubuntu-desktop mesa-utils
	export DISPLAY=localhost:0
	export LIBGL_ALWAYS_INDIRECT=1

install:
	curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
	$(HOME)/.rye/shims/rye sync --no-lock --no-dev

devinstall:
	curl -sSf https://rye-up.com/get | RYE_NO_AUTO_INSTALL=1 RYE_INSTALL_OPTION="--yes" bash
	$(HOME)/.rye/shims/rye pin $(PYTHON_VERSION)
	$(HOME)/.rye/shims/rye sync --no-lock

test:
	$(HOME)/.rye/shims/rye run pytest

run: 
	$(HOME)/.rye/shims/rye run python main.py

lint:
	$(HOME)/.rye/shims/rye lint -q -- --select I --fix 

format:
	$(HOME)/.rye/shims/rye fmt

all: devinstall lint format test
