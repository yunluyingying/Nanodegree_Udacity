import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie, Documentation
from datetime import date
from dotenv import load_dotenv

load_dotenv()

casting_assistant_auth_header = {
    "Authorization": "Bearer " +
    os.environ.get('TOKEN_CASTING_ASSISTANT', "")}
casting_director_auth_header = {
    "Authorization": "Bearer " +
    os.environ.get('TOKEN_CASTING_DIRECTOR', "")}
executive_producer_auth_header = {
    "Authorization": "Bearer " +
    os.environ.get('TOKEN_EXECUTIVE_PRODUCER', "")}


class CastAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "cast_agency_test"
        self.database_path = os.environ.get('DATABASE_URL',
                                            "postgres://{}/{}".format(
                                                'localhost:5432', self.database_name))
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    test for POST /actors
    """

    def test_create_new_actors(self):

        new_actor = {
            "name": "Mary Ann",
            "age": 25,
            "gender": "female"
        }
        res = self.client().post('/actors', json=new_actor,
                                 headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_auth_create_new_actors(self):

        new_actor = {
            "name": "Chris Lee",
            "age": 28,
            "gender": "male"
        }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers=casting_assistant_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication failed')

    def test_400_create_new_actors(self):

        new_actor = {
            "age": 28,
            "gender": "male"
        }

        res = self.client().post('/actors', json=new_actor,
                                 headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_new_actors_holder(self):

        new_actor = {
            "name": "Chris Lee",
            "age": 28,
            "gender": "male"
        }

        res = self.client().post(
            '/actors',
            json=new_actor,
            headers=executive_producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    """
    test for GET /actors
    """

    def test_get_all_actors(self):
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    """
    test for PATCH /actors
    """

    def test_update_actors(self):

        update_actor_age = {
            "age": 30
        }
        res = self.client().patch(
            '/actors/2',
            json=update_actor_age,
            headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_error_update_actors(self):

        update_actor_age = {
            "age": 30
        }
        res = self.client().patch(
            '/actors/145667',
            json=update_actor_age,
            headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    """
    test for DELETE /actors
    """

    def test_401_auth_delete_actors(self):

        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication failed')

    def test_delete_actors(self):

        res = self.client().delete('/actors/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        a = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertEqual(a, None)

    """
    test for POST /movies
    """

    def test_create_new_movies(self):

        new_movie = {
            "title": "Dragon I",
            "release_date": "2019-4-1"

        }
        res = self.client().post(
            '/movies',
            json=new_movie,
            headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_auth_create_new_movies(self):

        new_movie = {
            "title": "Dragon II",
            "release_date": "2020-4-1"
        }

        res = self.client().post('/movies', json=new_movie,
                                 headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication failed')

    def test_400_create_new_movies(self):

        new_movie = {
            "release_date": "2020-4-1"
        }

        res = self.client().post(
            '/movies',
            json=new_movie,
            headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_create_new_movies_holder(self):

        new_movie = {
            "title": "Dragon II",
            "release_date": "2020-4-1"

        }
        res = self.client().post(
            '/movies',
            json=new_movie,
            headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    """
    test for PATCH /movies
    """

    def test_update_movies(self):

        update_movie = {
            "release_date": str(date.today())
        }
        res = self.client().patch('/movies/2', json=update_movie,
                                  headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_error_update_movies(self):

        update_movie = {
            "release_date": str(date.today())
        }
        res = self.client().patch(
            '/movies/145667',
            json=update_movie,
            headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')

    """
    test for GET /movies
    """

    def test_get_all_movies(self):
        res = self.client().get('/movies', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    """
    test for DELETE /movies
    """

    def test_delete_movies(self):

        res = self.client().delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        m = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)
        self.assertEqual(m, None)

    def test_401_auth_delete_movies(self):

        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'authentication failed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
