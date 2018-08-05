install:
	pip install -r requirements.txt

run:
	gunicorn src.handler:app

test:
	DATABASE_NAME='mock.db' python -m unittest src.handler_test
