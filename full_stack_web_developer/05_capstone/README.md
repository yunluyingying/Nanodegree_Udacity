# Casting Agency APP

## Motivation

This is the final capstone project that was expected to cover topics of data modeling, API building and testing, authorization and deployment. The topic I selected is the casting agency API which serves as the documentation for actors and movies for casting personnels. Depending on the role, it would help the person to review the actors/movies info they are looking for.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get: actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get: movies`
    - `post:movies`
    - `patch:movies`
    - `delete:movies`
6. Create new roles for:
    - Casting Assistant
        - can `get: actors` and `get: movies`
    - Casting Director
        - can `get: actors`, `post:actors`, `patch:actors`, `delete:actors`, `get: movies`, and `patch:movies`
    - Executive Producer
        - can perform all actions

7. Test your endpoints locally.
    - Register 3 users and each one represents one role
    - Sign into each account and copy the JWT to the `utils.py`
```
    url: https://fsnd-yyc.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=4iM2KBaJfJ9UmrELFIzjnYfFRtAF2hZQ&redirect_uri=http://localhost:8100/callback
    test3: Casting Assistant
    test4: Casting Director
    test5: Executive Producer
```

### Deployment

## API Reference

### Getting Started
- Base URL: Heroku URL is https://capstone-cast-agency.herokuapp.com/
- Authentication: see the section above.

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

- 400: bad request
- 401: authentication failed
- 404: resource not found
- 422: unprocessable

### Endpoints

#### GET /actors

- General: Fetches a dictionary of actors
- Request Arguments: None
- Request Permission: `get: actors`
- Returns: An object with a list of actors (and detailed info), number of actors, and another boolean key success to indicate the status of connections.
- Sample:  ```curl -X GET https://capstone-cast-agency.herokuapp.com/actors -H "Authorization: Bearer ${token}"```

```
{"actors":
  [{"age":25,"gender":"female","id":1,"name":"Mary Ann"},
   {"age":28,"gender":"male","id":2,"name":"Chris Lee"}],
   "success":true,
   "total_actors":2}
```

#### POST /actors

- General: Create a new actor
- Request Arguments: the name, age and gender of an actor
- Request Permission: `post:actors`
- Returns: Returns the id of the created actor and his info, and success value,
- Sample:  ```curl -X POST https://capstone-cast-agency.herokuapp.com/actors -d '{
            "name": "Mary Ann",
            "age": 25,
            "gender": "female"}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${token}" ```

```
{"actor":{"age":25,"gender":"female","id":1,"name":"Mary Ann"},"success":true}
```

#### PATCH /actors/{actor_id}

- General: Update an existing actor
- Request Arguments: actor_id and the content to be updated
- Request Permission: `patch:actors`
- Returns: Returns the whole updated actor info, and success value,
- Sample:  ```curl -X PATCH https://capstone-cast-agency.herokuapp.com/actors/1 -d '{
            "age": 30}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${token}" ```

```
{"actor":{"age":30,"gender":"female","id":1,"name":"Mary Ann"},"success":true}
```

### DELETE /actors/{actor_id}

- General: Deletes the actor of the given ID if it exists
- Request Arguments: actor_id
- Request Permission: `delete:actors`
- Returns: Returns the id of the deleted actor and success value
- Sample:  ```curl -X DELETE https://capstone-cast-agency.herokuapp.com/actors/2 -H "Authorization: Bearer ${token}"```

```
{"delete":2,"success":true}
```

#### GET /movies

- General: Fetches a dictionary of movies
- Request Arguments: None
- Request Permission: `get: movies`
- Returns: An object with a list of movie titles, number of movies, and another boolean key success to indicate the status of connections.
- Sample:  ```curl -X GET https://capstone-cast-agency.herokuapp.com/movies -H "Authorization: Bearer ${token}"```

```
{"movies":["Dragon I","Dragon II"],"success":true,"total_movies":2}
```

#### POST /movies

- General: Create a new movie
- Request Arguments: the title and release date of the movie
- Request Permission: `post:movies`
- Returns: Returns the id of the created movie and related info, and success value,
- Sample:  ```curl -X POST https://capstone-cast-agency.herokuapp.com/movies -d '{
            "title": "Dragon I",
            "release_date": "2019-4-1"}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${token}" ```

```
{"movie":{"id":1,"release_date":"2019-4-1","title":"Dragon I"},"success":true}
```

#### PATCH /movies/{movie_id}

- General: Update an existing movie
- Request Arguments: movie_id and the content to be updated
- Request Permission: `patch:movies`
- Returns: Returns the whole updated actor info, and success value,
- Sample:  ```curl -X PATCH https://capstone-cast-agency.herokuapp.com/movies/1 -d '{
            "release_date": "2020-4-10"}' -H 'Content-Type: application/json' -H "Authorization: Bearer ${token}" ```

```
{"movie":{"id":1,"release_date":"2020-4-1","title":"Dragon I"},"success":true}
```

### DELETE /movies/{movie_id}

- General: Deletes the actor of the given ID if it exists
- Request Arguments: movie_id
- Request Permission: `delete:movies`
- Returns: Returns the id of the deleted movie and success value
- Sample:  ```curl -X DELETE https://capstone-cast-agency.herokuapp.com/movies/1 -H "Authorization: Bearer ${token}"```

```
{"delete":1,"success":true}
```


