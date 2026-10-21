.PHONY: up down logs test-api test-web lint migrate format

up:
	docker compose up -d --build --wait --wait-timeout 180

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f --tail=200

test-api:
	docker compose run --rm --no-deps api pytest -q

test-web:
	docker compose run --rm --no-deps web pnpm test

lint:
	docker compose run --rm --no-deps api sh -c "ruff check . && ruff format --check . && mypy src"
	docker compose run --rm --no-deps web sh -c "pnpm lint && pnpm typecheck"

migrate:
	docker compose run --rm api alembic upgrade head

format:
	docker compose run --rm --no-deps api sh -c "ruff check --fix . && ruff format ."
	docker compose run --rm --no-deps web pnpm format
