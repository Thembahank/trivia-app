import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

database_path = "postgres://{}/{}".format('localhost:5432', 'trivia_test')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all() # create all tables

        self.add_question = {"question": "2 vs four spaces",
                             "answer": "4 spaces",
                             "category": "1",
                             "difficulty": "2"}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions/?page=1000', json={'category': 4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_new_question(self):
        res = self.client().post('/questions/', json=self.add_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_delete_question(self):
        id = Question.query.first().id
        res = self.client().delete('/questions/{}/'.format(id))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_get_question_search_with_results(self):
        res = self.client().post('/questions/', json={"search_term":"dutch"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # expect that more than one question returned
        self.assertGreater(data['total_questions'],0)

    def test_get_question_search_without_results(self):
        res = self.client().post('/questions/', json={"search_term": "a*(&^(*&JJHlien"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # expect num of question returned from query to be nil
        self.assertEqual(data['total_questions'],0)

    def test_play_quiz_all_categories(self):
        res = self.client().post('/quizzes/', json={"previous_questions":[1,2], "quiz_category":{"type":"ALL", "id":"0"}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_quiz_in_one_categories(self):
        res = self.client().post('/quizzes/', json={"previous_questions": [], "quiz_category": {"type":"Sports", "id": "4"}})
        data = json.loads(res.data)

        res2 = self.client().post('/quizzes/',json={"previous_questions": [], "quiz_category": {"type": "Sports", "id": "3"}})
        data2 = json.loads(res2.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check that the questions returned from both categories are not the same
        self.assertNotEqual(data['question'],data2['question'])

    def test_404_if_question_does_not_exist(self):
        res = self.client().get('/questions/1000/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_422_if_question_creation_sent_failed(self):
        res = self.client().post('/questions/', json={"question": "sample"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_405_method_not_allowed_quizzes(self):
        res = self.client().get('/quizzes/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()