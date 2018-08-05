install:
	pip install -r requirements.txt

run:
	gunicorn src.handler:app

test:
	DATABASE_NAME='mock.db' python3 -m unittest src.handler_test
	DATABASE_NAME='test_db.db' python3 -m unittest src.db_test
