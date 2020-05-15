import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [q.format() for q in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route
    after completing the TODOs
    '''
    CORS(app, resources={r"api/*": {"origins": "*"}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', \
          'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', \
          'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''

    @app.route("/categories", methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories_list = {c.id: c.type for c in categories}

        res = {
            "success": True,
            "categories": categories_list
        }

        return jsonify(res)

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen
    for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route("/questions", methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.all()
        categories_list = [c.type for c in categories]

        if len(current_questions) == 0:
            aboort(404)

        res = {
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": categories_list,
            "current_category": None
        }

        return jsonify(res)

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question
    will be removed.
    This removal will persist in the database and when you refresh the
    page.
    '''

    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_questions(question_id):
        q = Question.query.filter(Question.id == question_id).\
            one_or_none()

        if not q:
            abort(404)

        try:
            q.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            res = {
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(selection)
            }

            return jsonify(res)

        except:
            abort(500)

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of
    the last page of the questions list in the "List" tab.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route("/questions", methods=['POST'])
    def create_or_search_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        if not body or (not new_question and not new_answer and \
            not new_difficulty and not new_category and not search):
            abort(400)

        if search:
            try:
                selection = Question.query.order_by(Question.id).filter(
                  Question.question.ilike(f"%{search}%")).all()
                if not selection:
                    return jsonify({
                      'success': True,
                      'questions': None,
                      'total_questions': 0

                    })
                elif len(selection) > 0:
                    current_questions = paginate_questions(request, selection)

                    return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(selection)
                        })
            except:
                abort(422)

        elif not search and new_question and new_answer and new_category\
         and new_difficulty:
            try:
                question = Question(question=new_question, answer=new_answer, \
                    category=new_category, difficulty=new_difficulty)
                question.insert()

                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                  'success': True,
                  'created': question.id,
                  'questions': current_questions,
                  'total_questions': len(selection)
                })

            except:
                abort(500)

        abort(422)

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route("/categories/<int:category_id>/questions", methods = ['GET'])
    def get_questions_by_category(category_id):
        selection = Question.query.filter(Question.category==category_id) \
                    .order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        res = {
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'current_category': category_id
              }

        return jsonify(res)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        body = request.get_json()

        if not body:
            abort(400)

        categories = Category.query.all()
        categories_set = {c.id for c in categories}


        previous_questions = body.get("previous_questions", None)
        current_category = body.get("quiz_category", None)

        question_list = []


        # handle the id = 0 for ALL category
        if current_category and current_category['id'] not in categories_set:
            current_category = None


        if previous_questions and current_category:
            question_list = Question.query \
                            .filter(Question.category==current_category['id'])\
                            .filter(Question.id.notin_(previous_questions)).all()
        elif previous_questions and not current_category:
            question_list = Question.query \
                            .filter(Question.id.notin_(previous_questions)).all()
        elif not previous_questions and current_category:
            question_list = Question.query \
                            .filter(Question.category==current_category['id']).all()
        elif not previous_questions and not current_category:
            question_list = Question.query.all()


        if len(question_list) != 0:
            random_question = random.choice([q.format() for q in question_list])
        else:
            random_question = ""


        return jsonify({
          "success": True,
          "question": random_question
          })



    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 400,
          "message": "bad request"
          }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "not found"
          }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "unprocessable"
          }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
          "success": False,
          "error": 500,
          "message": "internal server error"
          }), 500



    return app

