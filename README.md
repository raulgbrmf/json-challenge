# Json Challenge

The current version is responsible for extracting the body from a POST request, put in the appropriate Json format and after validation with the jsonschema return the Json output and store it in a sqlite database file.

As I was able to choose between Python or Java, I chose Python due to the simplicity to write a code in it and mainly because of Flask. Flask is a microframework written in Python that eases the learning curve to develop simple web applications. In my opinion, Python codes tends to be more clear to write and read than Java. As this challenge is a small web application I think these choices make sense.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run it you first need to install the tools listed in the requirements file.
Note that this program runs in Python 3.

```
make install
```

### Running

To run the application just run the Makefile using make run.

```
make run
```

### Testing

To test this application just run the Makefile using make test.

```
make test
```

To test it you can run a POST request on http://127.0.0.1:8000/post (or localhost:8000/post). ( You can use Postman to facilitate this operation.)
If your body content is in the appropriate format it will return it on screen in a Json format.
If not, it will display "Invalid Output."

To retrieve data that was stored by a POST request you can use a GET request on http://127.0.0.1:8000/version_id/db_name/logic_id (or localhost:8000/version_id/db_name/logic_id)

Finally, to change some information you can use a PUT request on http://127.0.0.1:8000/version_id/db_name/logic_id (or localhost:8000/version_id/db_name/logic_id) with a json content on the body of the request.

### Heroku

This API is also deployed by Heroku on : https://flask-json-challenge.herokuapp.com/
