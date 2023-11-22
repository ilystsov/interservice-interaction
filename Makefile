CODE_FOLDERS := server db config blacklist_server seed
TEST_FOLDERS := tests

.PHONY: install update test format lint db_upgrade db_seed db_start generate_client

install:
	poetry install

update:
	poetry lock

test:
	poetry run pytest $(TEST_FOLDERS)

format:
	black .

lint:
	black --check $(CODE_FOLDERS) $(TEST_FOLDERS)
	flake8 $(CODE_FOLDERS) $(TEST_FOLDERS)
	pylint $(CODE_FOLDERS) $(TEST_FOLDERS)
	mypy --follow-imports=silent $(CODE_FOLDERS) $(TEST_FOLDERS)

db_upgrade:
	alembic upgrade head

db_seed:
	python -m seed

db_start: db_upgrade db_seed

# OpenAPI Generator Docker image
OPENAPI_GENERATOR_IMAGE := openapitools/openapi-generator-cli

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
	sudo mv ./clients/${CLIENT}/clients/${CLIENT} ./clients/tmp_${CLIENT}
	sudo rm -rf ./clients/${CLIENT}
	sudo mv ./clients/tmp_${CLIENT} ./clients/${CLIENT}
	sudo rm openapi.json