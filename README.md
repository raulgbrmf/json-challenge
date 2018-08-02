# Json Challenge

This current version is responsible for extract the body from a POST request, put in the appropriate Json format and after the validation with the jsonschema return the Json output and store it in a sqlite database file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run it you first need to install the tools listed in the requirements file.

```
make install
```

### Running

To run the application just run the Makefile using the command make run.

```
make run
```

This version will run in debug mode on port 5000.

To test it you can run a POST request on http://127.0.0.1:5000/post (or localhost:5000/post). ( You can use Postman to facilitate this operation.)
If your body content is in the appropriate format it will return it on screen in a Json format.
If not, it will display "Invalid Output."

To retrieve data that was stored by a POST request you can use a GET request on http://127.0.0.1:5000/?version=version_id&entity=db_name&logic=logic_id (or localhost:5000/?version=version_id&entity=db_name&logic=logic_id)

Finally, to change some information you can use a PUT request on http://127.0.0.1:5000/?version=version_id&entity=db_name&logic=logic_id (or localhost:5000/?version=version_id&entity=db_name&logic=logic_id) with a json content on the body of the request.
