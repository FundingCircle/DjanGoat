.PHONY: install run lint test clean
deafult: install

install:
	(\
		pip install virtualenv; \
		virtualenv env --python=python2.7; \
		source env/bin/activate; \
		pip install -r requirements.txt; \
		python manage.py migrate; \
		python manage.py seed; \
	)

run:
	(\
		source env/bin/activate; \
		python manage.py migrate; \
		python manage.py runserver; \
	)

clean:
	rm -f db.sqlite3
	rm -rf env/

lint:
	(\
		source env/bin/activate; \
		pylint app pygoat; \
	)

test:
	coverage run manage.py test app
	coverage report
