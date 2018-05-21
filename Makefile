all:
	;

venv: requirements.txt requirements-dev.txt
	python3 -m virtualenv venv
	venv/bin/pip install -r requirements.txt -r requirements-dev.txt
	touch venv
