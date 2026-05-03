rebuild-backend:
    uv lock
    uv sync
    docker-compose -f compose/local/local.yml down
    docker volume rm dinx_local_fastapi_venv || true
    docker-compose -f compose/local/local.yml build --no-cache
    docker-compose -f compose/local/local.yml up

run:
    docker-compose -f compose/local/local.yml up

test:
    uv run pytest
