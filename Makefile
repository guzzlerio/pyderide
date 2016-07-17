build: install format test lint test

install:
	pip install -r requirements.txt

lint:
	pylint --rcfile pylint.rc deride.py 

test:
	nosetests --all-modules --traverse-namespace --with-coverage --cover-min-percentage=80 --cover-package=pyderide --cover-inclusive

format:
	autopep8 --in-place --aggressive --aggressive deride.py
	autopep8 --in-place --aggressive --aggressive test-deride.py


.PHONY: build
