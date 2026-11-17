GO_DIR := services/api
PY_DIR := services/ai
COMPOSE := docker compose -f deploy/docker-compose.yml
GOTESTFLAGS ?=

.PHONY: lint test lint-go lint-py test-go test-py fmt up down run-api

lint: lint-go lint-py

test: test-go test-py

lint-go:
	cd $(GO_DIR) && golangci-lint run ./...

test-go:
	go -C $(GO_DIR) test $(GOTESTFLAGS) ./...

lint-py:
	uv run --directory $(PY_DIR) ruff check .
	uv run --directory $(PY_DIR) ruff format --check .

test-py:
	uv run --directory $(PY_DIR) pytest

fmt:
	cd $(GO_DIR) && golangci-lint fmt ./...
	uv run --directory $(PY_DIR) ruff check --fix .
	uv run --directory $(PY_DIR) ruff format .

up:
	$(COMPOSE) up -d --wait

down:
	$(COMPOSE) down

run-api:
	go -C $(GO_DIR) run ./cmd/api
