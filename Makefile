.DEFAULT_GOAL := env

run : env
	.venv/bin/wire

env : .venv/bin/activate

.venv/bin/activate : requirements.txt
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install --upgrade pip wheel
	.venv/bin/pip install -Ur requirements.txt
	.venv/bin/pip install --editable .
	touch .venv/bin/activate


env_dev : env .venv/has_dev

.venv/has_dev : requirements_dev.txt
	.venv/bin/pip install -Ur requirements_dev.txt
	touch .venv/has_dev # I don't understand makefiles send help

dev : isort black mypy test flake8 pylint

black : env_dev
	.venv/bin/black wire
	.venv/bin/black tests

mypy : env_dev
	.venv/bin/mypy wire
	.venv/bin/mypy tests

flake8 : env_dev
	.venv/bin/flake8 --ignore=E501 wire
	.venv/bin/flake8 --ignore=E501 tests

test : env_dev
	.venv/bin/coverage run --source=wire .venv/bin/pytest tests
	.venv/bin/coverage report

isort : env_dev
	.venv/bin/isort wire
	.venv/bin/isort tests

pylint : env_dev
	.venv/bin/pylint wire
	.venv/bin/pylint tests

clean :
	rm -rf .venv
	rm -rf wire.egg-info
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	find . -name "__pycache__" -type d -exec rm -rf {} +

