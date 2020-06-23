# Full Stack Trivia API Backend

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

## API reference

### Error Handling

Errors are returned as JSON objects in the format that follows:
```
{
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
}

The error types handled are as follows:

* 404: Not Found
* 405: Method Not Allowed
* 422: Unprocessable Entity
* 500: Internal Server Error
```

### All Endpoints

DELETE /questions/{question_id}

GET /categories

GET /questions

GET /categories/{category_id}/questions

POST /questions

POST /quizzes

### DELETE Enpoints

#### DELETE /questions/{question_id}

* General:
    * Deletes question of given id from database
    * returns on success:
        1. Id of deleted question
        1. List of questions, paginated in groups of 10
        1. Success key with Bool value
        1. Total number of questions after deletion operation
    * Sample: curl -X http://127.0.0.1:5000/questions/1
```
{
  "deleted_question": 33,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
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
    }
  ],
  "success": true,
  "total_questions": 18
}
```

### GET Endpoints

#### GET /categories
* General:
    * Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string if the category
    * Request Arguments: None
    * Returns an JSON object on success containing the following:
        1. Success status
        1. A dictionary containing all categories
        1. Total number of categories
    * Sample: curl http://127.0.0.1:5000/categories
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

#### GET /questions
* General:
    * Fetches and returns questions JSON payload
    * Returns on success:
        1. Success status
        1. Dictionary of current questions, paginated in groups of 10
        1. Number of total questions in database
        1. List of all categories
        1. Current category if applicable
    * Sample: curl http://127.0.0.1:5000/questions
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
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
    }
  ],
  "success": true,
  "total_questions": 18
}
```

#### GET /categories/{category_id}/questions
* General:
    * Fetches and returns questions JSON payload of a specified category id
    * Returns on success:
        1. Success status
        2. Id of selected category
        3. list of questions based on choosen category, paginated in groups of 10
        4. Number of total questions in selected category
    * Sample: curl http://127.0.0.1:5000/categories/4/questions
```
{
  "current_category": 4, 
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

### POST Endpoints

#### POST /questions
* General:
    * Does one of two options:
        * Creates question and inserts into database, returning JSON payload on success
        * Searches database by given category and returns JSON payload containing questions from that category
    * Returns on successful question insertion:
        1. Success status
        1. Id of created question
        1. List of current questions, paginated in groups of 8
        1. Number of total questions in database
    * Returns on successful category search:
        1. Success status
        1. Dictionary of questions from search category
        1. Number of total questions in search category
        1. Id of search category
    * Sample: curl -X POST -H "Content-Type: application/json" -d '{"question":"How many championships did Michael Jordan win with the Chicago Bulls?", "answer":"six", "category":"6", "difficulty":1}' http://127.0.0.1:5000/questions
```
{
  "created_question": 36,
  "questions": [
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
    }
  ],
  "success": true,
  "total_questions": 19
}
```

#### POST /quizzes
* General:
    * Fetches and returns JSON payload containing quiz questions based on choosen category
    * Returns on success:
        1. Success status
        1. Category specified
        1. Current quiz question of specified category
    * Sample: curl -X POST "Content-Type: application/json" -d '{"previous_questions":[], "quiz_category":{"type":"Art", "id":"2"}}' http://127.0.0.1:5000/questions

```
{
  "current_category": "Art",
  "question": {
    "answer": "Escher",
    "category": 2,
    "difficulty": 1,
    "id": 16,
    "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
  },
  "success": true
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```