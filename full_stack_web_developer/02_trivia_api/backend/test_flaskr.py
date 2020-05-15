import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
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
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(len(data['questions']))

    def test_error_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/question?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        q = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 2)
        self.assertTrue(data['total_questions'])
        self.assertEqual(q, None)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_create_new_question(self):

        new_question = {
            "question": "What is this question for?",
            "answer": "Test",
            "category": 1,
            "difficulty": 1
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_422_if_question_creation_fails(self):

        invalid_question = {
            "question": "Is this quesion valid?",
            "answer": "No",
            "difficulty": 1
        }

        res = self.client().post('/questions', json=invalid_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_search_question_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'What'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_search_question_without_results(self):
        res = self.client().post(
            '/questions', json={'searchTerm': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['questions'], None)

    def test_400_send_bad_request(self):
        res = self.client().post('/questions', json={'test': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], 1)
        self.assertTrue(len(data['questions']))

    def test_play_quiz_with_cat_and_previous_question(self):
        quiz1 = {
            "previous_questions": [1, 2],
            "quiz_category": {
                "id": 1,
                "type": "Science"
            }
        }

        res = self.client().post("/quizzes", json=quiz1)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 1)
        self.assertTrue(data['question']['id']
                        not in quiz1["previous_questions"])

    def test_play_quiz_with_no_cat_and_previous_question(self):
        quiz2 = {
            "previous_questions": [1, 2, 4],
            "quiz_category": {
                "id": 0,
                "type": "Click"
            }
        }

        res = self.client().post("/quizzes", json=quiz2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['id']
                        not in quiz2["previous_questions"])

    def test_play_quiz_with_no_cat_and_no_previous_question(self):
        quiz3 = {
            "previous_questions": [],
            "quiz_category": {
                "id": 0,
                "type": "Click"
            }
        }

        res = self.client().post("/quizzes", json=quiz3)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_quiz_with_cat_no_question_left(self):
        quiz4 = {
            "previous_questions": [10, 11],
            "quiz_category": {
                "id": 6,
                "type": "Sports"
            }
        }

        res = self.client().post("/quizzes", json=quiz4)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], "")

    def test_400_play_quiz_with_bad_request(self):

        res = self.client().post("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
