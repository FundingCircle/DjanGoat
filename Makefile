.PHONY: install run test clean
deafult: clean install run

install:
	(\
		pip install virtualenv; \
		virtualenv env --python=python3.7; \
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
	rm -rf src/

test:
	coverage run manage.py test app
	coverage report
