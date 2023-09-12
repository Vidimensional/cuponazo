.PHONY: test unittest
test: unittest
unittest:
	@python -m coverage run -m unittest discover -s ./test/unit/ -p '*.py'

.PHONY: coverage report-coverage html-coverage html
coverage: unittest report-coverage
report-coverage:
	@python -m coverage report --omit='test/*'
html: html-coverage
html-coverage: unittest
	@python -m coverage html --omit='test/*'

.PHONY: dev-dependencies dependencies dep
dep: dependencies dev-dependencies
dependencies:
	@python -m pip install -r requirements.txt
dev-dependencies:
	@python -m pip install -r requirements-dev.txt
