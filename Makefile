
clean:
	rm -rf .venv

venv: clean
	python --version
	python -m venv .venv
	poetry install

	echo "To activate, use 'source ./.venv/bin/activate'"
	echo "To deactivate, use 'deactivate'"


data:
	echo TODO


test:
	poetry run pytest google_takeout/tests