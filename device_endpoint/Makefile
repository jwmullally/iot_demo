all:
	;

venv: requirements.txt
	python3 -m virtualenv venv
	venv/bin/pip install -r requirements.txt
	touch venv

shell: venv
	venv/bin/ipython

run: venv
	venv/bin/python -m device_endpoint

clean:
	rm -rf venv dist build *.egg-info .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type f -name "*.pyc" -delete

