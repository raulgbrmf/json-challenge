install:
	pip3 install -r requirements.txt

run:
	gunicorn src.handler:app

test:
	DATABASE_NAME='mock.db' python3 -m unittest src.handler_test
