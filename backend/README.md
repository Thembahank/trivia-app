# Trivia API backend

Welcome to the trivia API. You can use this API to access our categories, quizzes and questions API endpoints.
The API is organized around REST. All request and response bodies, including errors, encoded in JSON.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder.
 Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. 
 If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

# heroku db
heroku login
heroku pg:reset DB_URL_HERE
heroku psql DB_URL_HERE < ./trivia.psql --app=app_name
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. 
The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
  "error": 404,
  "message": "Resource not found",
  "success": false
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: unprocessable 
- 405: Method not allowed
- 500: Server error

### Endpoints 
#### GET /categories/
- General:
    - Returns a list of categories & success value
- Sample: `curl http://127.0.0.1:5000/categories/`

```
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```

#### GET /questions/
- General:
    - Returns a list of questions, success value, total number of questions, total in page and all the categories
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions/`

``` 
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "current_category": 1,
  "current_page": 1,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_in_page": 10,
  "total_questions": 22
}
```

#### POST /questions/
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, 
    success value, total questions, and questions list based on current page number to update the frontend. 
-Sample: `curl http://127.0.0.1:5000/questions/?page=2 -X POST -H "Content-Type: application/json" -d '{"question": "2 vs four spaces","answer": "4 spaces","category": "2","difficulty": "2"}'`
```
{
	"created": 30,
	"current_page": 2,
	"current_questions":[
		{
			"answer": "Agra",
			"category": 3,
			"difficulty": 2,
			"id": 15,
			"question": "The Taj Mahal is located in which Indian city?"
		},
		{"answer": "Escher", "category": 2, "difficulty": 1, "id": 16, "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"…},
		{"answer": "Mona Lisa", "category": 2, "difficulty": 3, "id": 17, "question": "La Giaconda is better known as what?"…},
		{"answer": "One", "category": 2, "difficulty": 4, "id": 18, "question": "How many paintings did Van Gogh sell in his lifetime?"…},
		{"answer": "Jackson Pollock", "category": 2, "difficulty": 2, "id": 19,…},
		{"answer": "The Liver", "category": 1, "difficulty": 4, "id": 20, "question": "What is the heaviest organ in the human body?"…},
		{"answer": "Alexander Fleming", "category": 1, "difficulty": 3, "id": 21,…},
		{"answer": "Blood", "category": 1, "difficulty": 4, "id": 22, "question": "Hematology is a branch of medicine involving the study of what?"…},
		{"answer": "Scarab", "category": 4, "difficulty": 4, "id": 23, "question": "Which dung beetle was worshipped by the ancient Egyptians?"…},
		{"answer": null, "category": null, "difficulty": null, "id": 24, "question": "askme"…}
	],
	"success": true,
	"total_in_page": 10,
	"total_questions": 26
}
```
#### POST /questions/
- General:
    - Searches for questions matching a provided string. Returns 
    success value, total questions, and questions list based on current page number to update the frontend.
- Sample:`curl http://127.0.0.1:5000/questions/?page=2 -X POST -H "Content-Type: application/json" -d '{"search_term": "2 vs four spaces"}`
 
 ```
{
	"current_category": "ALL",
	"questions":[
		{
		"answer": "4 spaces",
		"category": 1,
		"difficulty": 2,
		"id": 26,
		"question": "2 vs four spaces"
		},
		{"answer": "4 spaces", "category": 2, "difficulty": 2, "id": 27, "question": "2 vs four spaces"…},
		{"answer": "3 spaces", "category": 2, "difficulty": 2, "id": 28, "question": "2 vs four spaces"…},
		{"answer": "3 spaces", "category": 2, "difficulty": 2, "id": 29, "question": "2 vs four spaces"…},
		{"answer": "3spaces", "category": 2, "difficulty": 2, "id": 30, "question": "2 vs four spaces"…}
	],
	"success": true,
	"total_questions": 5
}
```

#### DELETE /question/{question_id}
- General:
    - Deletes the question of the given ID if it exists. 
    Returns the id of the deleted question, success value, total questions,page number and current_questions 
- `curl -X DELETE http://127.0.0.1:5000/questions/11/?page=2`
```
{
	"current_page": 2,
	"current_questions":[
		{
			"answer": "Mona Lisa",
			"category": 2,
			"difficulty": 3,
			"id": 17,
			"question": "La Giaconda is better known as what?"
		},
		{
			"answer": "One",
			"category": 2,
			"difficulty": 4,
			"id": 18,
			"question": "How many paintings did Van Gogh sell in his lifetime?"
		},
		{"answer": "Jackson Pollock", "category": 2, "difficulty": 2, "id": 19,…},
		{"answer": "The Liver", "category": 1, "difficulty": 4, "id": 20, "question": "What is the heaviest organ in the human body?"…},
		{"answer": "Alexander Fleming", "category": 1, "difficulty": 3, "id": 21,…},
		{"answer": "Blood", "category": 1, "difficulty": 4, "id": 22, "question": "Hematology is a branch of medicine involving the study of what?"…},
		{"answer": "Scarab", "category": 4, "difficulty": 4, "id": 23, "question": "Which dung beetle was worshipped by the ancient Egyptians?"…},
		{"answer": null, "category": null, "difficulty": null, "id": 24, "question": "askme"…},
		{"answer": null, "category": null, "difficulty": null, "id": 25, "question": "askme"…},
		{"answer": "4 spaces", "category": 1, "difficulty": 2, "id": 26, "question": "2 vs four spaces"…}
	],
	"deleted": 11,
	"success": true,
	"total_in_page": 10,
	"total_questions": 24
}
```

#### POST /questions/
- General:
    - Searches for questions matching a provided string. Returns
    success value, total questions, and questions list based on current page number to update the frontend.
- `curl http://127.0.0.1:5000/questions/?page=2 -X POST -H "Content-Type: application/json" -d '{"search_term": "2 vs four spaces"}`
 
 ```
{
	"current_category": "ALL",
	"questions":[
		{
		"answer": "4 spaces",
		"category": 1,
		"difficulty": 2,
		"id": 26,
		"question": "2 vs four spaces"
		},
		{"answer": "4 spaces", "category": 2, "difficulty": 2, "id": 27, "question": "2 vs four spaces"…},
		{"answer": "3 spaces", "category": 2, "difficulty": 2, "id": 28, "question": "2 vs four spaces"…},
		{"answer": "3 spaces", "category": 2, "difficulty": 2, "id": 29, "question": "2 vs four spaces"…},
		{"answer": "3spaces", "category": 2, "difficulty": 2, "id": 30, "question": "2 vs four spaces"…}
	],
	"success": true,
	"total_questions": 5
}
```
#### POST /quizzes/
- General:
    -  This endpoint takes a quiz_category {} and previous_questions [] parameters and returns a random question within the given category, 
    if provided. The question returned will not be one of whose ID is supplied in the previous_questions list
- `curl http://127.0.0.1:5000/quizzes/ -X POST -H "Content-Type: application/json" -d '"previous_questions":[1,2], "quiz_category":{"type":"ALL", "id":"0"}}`
 
 ```
{
	"question":{
		"answer": "Maya Angelou",
		"category": 4,
		"difficulty": 2,
		"id": 5,
		"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
	},
	"success": true
}
```

## Authors
Thembelani Mahlangu

## Acknowledgements 

Udacity team, and Caryn McCarthy @ Udacity for guidance on best practices for API documentation

