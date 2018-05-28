all:
	;

venv: requirements.txt requirements-dev.txt
	python3 -m virtualenv venv
	venv/bin/pip install -r requirements.txt -r requirements-dev.txt
	touch venv

db: venv
	venv/bin/python manage.py makemigrations
	venv/bin/python manage.py migrate
	venv/bin/python manage.py loaddata test_data

shell: venv db
	venv/bin/python manage.py shell

runserver: venv db
	venv/bin/python manage.py runserver

test: venv
	venv/bin/python manage.py test
	-venv/bin/pylint --load-plugins pylint_django iot_site *.py

clean:
	rm -rf venv db.sqlite3 dist build *.egg-info .coverage
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type f -name "*.pyc" -delete
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
