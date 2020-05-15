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


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Erros are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three error types when requests fail:

- 400: Bad Request
- 404: Not Found
- 422: Not Processable
- 500: internal server error

### Endpoints

#### GET /categories

- General: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a key, categories, that contains a object of id: type pairs and another boolean key success to indicate the status of connections.
- Sample:  ```curl http://127.0.0.1:5000/categories```

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
  "success": true
}
```

#### GET /questions

- General: Returns a object of questions which are composed of different property keys. The results would be paginated in group of 10.
- Request Arguments: None or could include a request argument to choose page number starting from 1.
- Returns: An object with keys of categories, current_category, questions, success and number of total questions.
- Sample:  ```curl http://127.0.0.1:5000/questions```

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
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    ...
  ],
  "success": true,
  "total_questions": 19
}

```

### DELETE /questions/{question_id}

- General: Deletes the question of the given ID if it exists
- Request Arguments: question_id
- Returns: Returns the id of the deleted question, success value, total questions, and question list based on current page number to update the frontend.
- Sample:  ```curl -X DELETE http://127.0.0.1:5000/questions/2```

```
{
  "deleted": 2,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ],
  "success": true,
  "total_questions": 18
}
```

#### POST /questions

##### Create a question

- General: Create a new question
- Request Arguments: the question and answer text, category, and difficulty score
- Returns: Returns the id of the created question, success value, total questions, and question list based on current page number to update the frontend.
- Sample:  ```curl -X POST http://127.0.0.1:5000/questions -d '{"question": "What is this question for?", "answer": "Test", "category": 1, "difficulty": 1 }' -H 'Content-Type: application/json' ```

```
{
  "created": 24,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    ...
  ],
  "success": true,
  "total_questions": 19
}
```
##### Search a question

- General: Fetch questions based on a search term.The results would be paginated in group of 10.
- Request Arguments: Search item
- Returns: Returns the matched question, success value, total questions
- Sample:  ```curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm": "What" }' -H 'Content-Type: application/json' ```

```
{
  "questions": [
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
    ...
  ],
  "success": true,
  "total_questions": 8
}
```
6. Create a POST endpoint to get questions based on category.

#### GET /categories/<category_id>/questions

- General: Get questions based on category. The results would be paginated in group of 10.
- Request Arguments: cateogry_id
- Returns: An object with keys of current_category, questions, success and number of total questions.
- Sample:  ```curl http://127.0.0.1:5000/categories/1/questions```

```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Test",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "What is this question for?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

#### POST /quizzes

- General: Get questions to play the quiz
- Request Arguments: None
- Returns: Return a random question within the given category if provided and not showing the previous questions if having any and success value
- Sample:  ```curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions": [1,2]}' -H 'Content-Type: application/json' ```

```
{
  "question": {
    "answer": "Scarab",
    "category": 4,
    "difficulty": 4,
    "id": 23,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}
```

## Deployment N/A

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

Outcome should be like:
```
............
----------------------------------------------------------------------
Ran 16 tests in  0.787s

OK
```
