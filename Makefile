.DEFAULT_GOAL := wire

env : .venv/bin/activate

.venv/bin/activate : requirements.txt
	test -d .venv || python3 -m venv .venv
	.venv/bin/pip install --upgrade pip wheel
	.venv/bin/pip install -Ur requirements.txt

env_dev : env .venv/has_dev

.venv/has_dev : requirements_dev.txt
	.venv/bin/pip install -Ur requirements_dev.txt
	touch .venv/has_dev # touch this se we don't have to reinstall each time

wire : env
	.venv/bin/pip install --editable .

dev : black mypy flake8 test

black : env_dev
	.venv/bin/black wire
	.venv/bin/black tests

mypy : env_dev
	.venv/bin/mypy wire
	.venv/bin/mypy tests

flake8 : env_dev
	.venv/bin/flake8 wire
	.venv/bin/flake8 tests

test : env_dev
	.venv/bin/pytest tests

clean :
	rm -rf .venv
	rm -rf wire.egg-info

