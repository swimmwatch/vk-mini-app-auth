SRC_DIR=.
TESTS_DIR=tests
PACKAGE_DIR=vk_miniapp_auth
REFERENCES_DIR=./docs/references
PYENV_VERSION ?= 3.13.12
POETRY := PYENV_VERSION=$(PYENV_VERSION) poetry
MKDOCS_ADDR ?= localhost:8010

mypy:
	$(POETRY) run mypy --config formatters-cfg.toml $(SRC_DIR)

flake:
	$(POETRY) run flake8 --toml-config formatters-cfg.toml $(SRC_DIR)

black:
	$(POETRY) run black --config formatters-cfg.toml $(SRC_DIR)

black-lint:
	$(POETRY) run black --check --config formatters-cfg.toml $(SRC_DIR)

isort:
	$(POETRY) run isort --settings-path formatters-cfg.toml $(SRC_DIR)

format: black isort

lint: flake mypy black-lint

lock:
	$(POETRY) lock

install:
	$(POETRY) install --no-root

mkdocs-serve:
	$(POETRY) run mkdocs serve --dev-addr $(MKDOCS_ADDR)

mkdocs-deploy:
	$(POETRY) run mkdocs gh-deploy --force

test:
	$(POETRY) run pytest --benchmark-autosave --cov=$(PACKAGE_DIR) --cov-branch --cov-report=xml --numprocesses logical $(TESTS_DIR)

actionlint:
	docker run --rm -v $(shell pwd):/repo --workdir /repo rhysd/actionlint:latest -color
