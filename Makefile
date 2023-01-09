clean:
	rm -rf dist build __pycache__ *.egg-info

format:
	poetry run isort src tests
	poetry run black --line-length=120 src tests

lint:
	poetry run black --check --diff --line-length=120 src tests
	poetry run pydocstyle src tests
	poetry run flake8 src tests
	poetry run mypy src
	poetry run pylint --rcfile=.pylintrc src tests

publish:
	make clean
	poetry build
	poetry publish

test-publish:
	make clean
	poetry build
	poetry publish -r test-pypi

.PHONY: tests
tests:
	poetry run pytest -vv

