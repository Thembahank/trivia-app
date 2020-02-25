import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # set up CORS on all origins
    CORS(app, resources={r"/*": {"origins": "*"}})

    # set response headers
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type , Authorization, Data-Type",)
        response.headers.add("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, PATCH, OPTIONS")
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    def paginate(request, selection):
        """paginate selection queryset based on page param provided in request"""
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions , page

    @app.route('/categories/', methods=['GET'])
    def categories():
        """return all available categories"""

        if request.method == 'GET':
            categories = Category.query.all()

            return jsonify({
                'success': True,
                'categories': [category.type for category in categories]
            })

    @app.route('/categories/<int:category_id>/questions/', methods=['GET'])
    def question_by_category(category_id):
        """return list of questions filtered by category"""

        # filter question by category, category is stored as varchar in questions, use str
        questions = Question.query.filter(Question.category == str(category_id)).all()

        if questions is None:
            return abort(404)

        else:
            current_questions, page = paginate(request, questions)
            formatted_questions = [q.format() for q in questions]

            categories = Category.query.order_by(Category.id).all()
            category = Category.query.filter(Category.id == category_id).one_or_none()

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'current_page': page,
                'categories': [c.type for c in categories],
                'current_category': category.type,
                'total_questions': len(formatted_questions),
                'total_in_page': len(current_questions),
                'questions': current_questions
            })

    @app.route('/questions/', methods=['GET', 'POST'])
    def questions():
        """
        GET: retrieve all questions
        POST: search for questions by field question
        POST: create a new question
        """

        if request.method == 'GET':
            questions = Question.query.all()
            current_questions, page = paginate(request, questions)
            formatted_questions = [q.format() for q in questions]

            categories = Category.query.all()

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'current_page':page,
                'categories':[c.type for c in categories],
                'current_category':1,
                'total_questions':len(formatted_questions),
                'total_in_page':len(current_questions),
                'questions': current_questions
            })

        if request.method == 'POST':

            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            category = body.get('category', None)
            difficulty = body.get('difficulty', None)

            search = body.get('search_term', None)

            try:
                # search for a question
                if search:
                    selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
                    current_questions, page = paginate(request, selection)

                    # if only one item assign category to that item else 'ALL'
                    category = 'ALL'
                    if len(current_questions) == 1:
                        category_id = current_questions[0]['category']
                        category_n = Category.query.filter(Category.id==category_id).one_or_none()
                        category = category_n.type if category_n is not None else category

                    return jsonify({
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(selection),
                        'current_category': category,
                    })

                else:

                    # reject if any of the fields are missing
                    if question is None or answer is None or category is None or difficulty is None:
                        abort(422)

                    # create a new book
                    question_obj = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                    question_obj.insert()
                    selection = Question.query.order_by(Question.id).all()
                    current_questions, page = paginate(request, selection)

                    return jsonify({
                        'success': True,
                        'created': question_obj.id,
                        'current_questions': current_questions,
                        'total_questions': len(Question.query.all()),
                        'total_in_page': len(current_questions),
                        'current_page': page,
                    })

            except:
                abort(422)

    @app.route('/questions/<int:question_id>/', methods=['GET', 'DELETE'])
    def question(question_id):

        """
        GET: retrieve  question by id
        DELETE: remove question
        """

        if request.method == 'GET':
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                return abort(404)

            else:
                return jsonify({
                    'success': True,
                    'question': question.format()
                })

        if request.method == 'DELETE':
            try:
                question = Question.query.filter(Question.id == question_id).one_or_none()

                if question is None:
                    abort(404)

                question.delete()
                selection = Question.query.order_by(Question.id).all()
                current_questions, page = paginate(request, selection)

                return jsonify({
                    'success': True,
                    'deleted':question_id,
                    'current_questions': current_questions,
                    'total_questions': len(selection),
                    'total_in_page': len(current_questions),
                    'current_page': page,
                })

            except:
                abort(422)

    @app.route('/quizzes/', methods=['POST'])
    def quizzes():
        """Returns questions given category, excludes questions in previous_questions param"""

        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        # query to pass down the control flow and filter if applicable
        query = None
        try:
            # filter by quiz category if we are not search for all
            if quiz_category and quiz_category['id'] not in ['0',0]:
                query = Question.query.filter(Question.category == str(quiz_category['id']))

            # filter to exclude previous questions if applicable
            if previous_questions and len(previous_questions) > 0:
                query = Question.query.filter(~Question.id.in_(previous_questions)) \
                    if query is None else query.filter(~Question.id.in_(previous_questions))

            selection = Question.query.all() if query is None else query.all()
            current_questions, page = paginate(request, selection)

            return jsonify({
                'success': True,
                'question': current_questions[0] if len(current_questions) > 0 else None,
            })

        except:
            abort(404)

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found",
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable",
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request",
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error",
        }), 500

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed",
        }), 405

    return app
