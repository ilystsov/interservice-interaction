CODE_FOLDERS := server db config
TEST_FOLDERS := tests

.PHONY: update test lint security_checks

install:
	poetry install

update:
	poetry lock

test:
	poetry run pytest $(TEST_FOLDER)

format:
	black .

lint:
	black --check .
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy $(CODE_FOLDERS) $(TEST_FOLDERS)

db_upgrade:
	alembic upgrade head

db_seed:
	python -m seed

db_start: db_upgrade db_seed

# OpenAPI Generator Docker image
OPENAPI_GENERATOR_IMAGE := openapitools/openapi-generator-cli

.PHONY: generate_client
generate_client:
	curl -o openapi.json ${DESCRIPTOR}
	docker run --rm \
		-v ${PWD}\:${PWD} \
		-w ${PWD} \
		${OPENAPI_GENERATOR_IMAGE} generate \
		-i openapi.json \
		-g python-pydantic-v1 \
		-o ./clients/${CLIENT} \
		--package-name clients.${CLIENT}
