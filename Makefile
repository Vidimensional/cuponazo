.PHONY: test unittest
test: unittest
unittest:
	python -m unittest discover -s ./test/unit/ -p '*.py'

.PHONY: dev-dependencies dependencies
dependencies:
	python -m pip install -r requirements.txt
dev-dependencies: dependencies
	python -m pip install -r requirements-dev.txt
