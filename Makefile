.PHONY: up down logs test-api test-web lint migrate format db-role coverage coverage-domain cleanup observability-up observability-down

up: db-role
	docker compose up -d --build --wait --wait-timeout 180

db-role:
	docker compose up -d --wait postgres
	docker compose exec -T postgres sh -c 'psql -U "$$POSTGRES_USER" -d "$$POSTGRES_DB" -f /docker-entrypoint-initdb.d/01-app-role.sql'

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

coverage:
	docker compose run --rm --no-deps api pytest --cov=tricolink --cov-report=term-missing --cov-fail-under=85

coverage-domain:
	docker compose run --rm --no-deps api sh -c "coverage run -m pytest -q && coverage report --include='*/domain/*' --fail-under=90"

cleanup:
	docker compose run --rm api python -m tricolink.jobs.cleanup

observability-up:
	mkdir -p .secrets
	docker compose exec -T api sh -c 'printf %s "$$METRICS_TOKEN"' > .secrets/metrics_token
	docker compose --profile observability up -d prometheus grafana

observability-down:
	docker compose --profile observability down
