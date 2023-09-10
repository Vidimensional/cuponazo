.PHONY: test unittest
test: unittest
unittest:
	python -m unittest discover -s test

