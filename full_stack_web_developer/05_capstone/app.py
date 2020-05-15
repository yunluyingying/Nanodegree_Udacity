import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie, Documentation
from flask_cors import CORS
from auth.auth import AuthError, requires_auth



def paginate_items(request, selection, ITEM_PER_PAGE = 10):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEM_PER_PAGE
    end = start + ITEM_PER_PAGE

    item = [q.format() for q in selection]
    current_items = item[start:end]

    return current_items


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    '''
    @Get actors
    Create an endpoint to handle GET requests
    for all available actors.
    '''
    @app.route("/actors", methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        selection = Actor.query.order_by(Actor.id).all()
        actors_paginated = paginate_items(request, selection, 10)

        if len(actors_paginated) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "actors": actors_paginated,
            "total_actors": len(selection)
        })

    '''
    @Create actors
    Create an endpoint to handle POST requests
    for creating an actor.
    '''
    @app.route("/actors", methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(payload):
        body = request.get_json()
        if not body:
            abort(400)
        new_name = body.get('name', None)
        new_gender = body.get('gender', None)
        new_age = body.get('age', None)

        if not new_name:
            abort(400)

        try:
            new_actor = Actor(name=new_name, gender=new_gender,
                              age=new_age)
            new_actor.insert()

            return jsonify({
                'success': True,
                'actor': new_actor.format()
            })

        except BaseException:
            abort(422)

    '''
    @Edit actors
    Create an endpoint to handle POST requests
    for editing an actor.
    '''
    @app.route("/actors/<int:actor_id>", methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, actor_id):

        body = request.get_json()
        if not body:
            abort(400)

        updated_name = body.get('name', None)
        updated_gender = body.get('gender', None)
        updated_age = body.get('age', None)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        if updated_name:
            actor.name = updated_name
        if updated_gender:
            actor.gender = updated_gender
        if updated_age:
            actor.age = updated_age

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

        '''
    @DELETE actors
    Create an endpoint to handle DELEET requests
    for removing an actor.
    '''
    @app.route("/actors/<int:actor_id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if not actor:
            abort(404)

        actor.delete()

        return jsonify({
            'success': True,
            'delete': actor.id
        })

    '''
    @Get movies
    Create an endpoint to handle GET requests
    for all available movies.
    '''
    @app.route("/movies", methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.order_by(Movie.id).all()

        if len(movies) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "movies": [m.title for m in movies],
            "total_movies": len(movies)
        })

    '''
    @Create movies
    Create an endpoint to handle POST requests
    for creating an movie.
    '''
    @app.route("/movies", methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(payload):
        body = request.get_json()
        if not body:
            abort(400)
        new_title = body.get('title', None)
        new_dt = body.get('release_date', None)

        if not new_title:
            abort(400)

        try:
            new_movie = Movie(title=new_title, release_date=new_dt)
            new_movie.insert()

            return jsonify({
                'success': True,
                'movie': new_movie.format()
            })
        except BaseException:
            abort(422)

    '''
    @Edit movies
    Create an endpoint to handle POST requests
    for editing an movie.
    '''
    @app.route("/movies/<int:movie_id>", methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload, movie_id):

        body = request.get_json()
        if not body:
            abort(400)

        updated_title = body.get('title', None)
        updated_dt = body.get('release_date', None)

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        if updated_title:
            movie.title = updated_title
        if updated_dt:
            movie.release_date = updated_dt

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format()
        })

        '''
    @DELETE movies
    Create an endpoint to handle DELEET requests
    for removing an movie.
    '''
    @app.route("/movies/<int:movie_id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if not movie:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'delete': movie.id
        })

    # Error Handling
    '''
    Error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    Error handling for not found
    '''
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    Error handling for bad request
    '''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    '''
    Error handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def auth_error(AuthError):
        return jsonify({
            "success": False,
            "error": AuthError.status_code,
            "message": "authentication failed"
        }), 401

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
