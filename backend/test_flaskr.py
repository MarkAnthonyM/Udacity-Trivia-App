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
        self.database_path = "postgres://{}:{}@{}/{}".format('markanthony', 'smokedl', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'answer': "Lake Victoria",
            'category': 3,
            'difficulty': 2,
            'question': "What is the largest lake in Africa?",
        }

        self.incomplete_question = {
            'answer': "",
            'category': 1,
            'difficulty': 2,
            'question': "What is the speed of light?"
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    # def test_404_get_categories(self):
    #     response = self.client().get('/categories')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], "Resource Not Found")

    def test_get_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertIsNone(data['current_category'])
        self.assertTrue(len(data['categories']))

    def test_404_get_invalid_question_page(self):
        response = self.client().get('/questions?page=100')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")

    def test_get_category_questions(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 1)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_create_question(self):
        response = self.client().post('/questions', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_question'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_405_invalid_create_question_post(self):
        response = self.client().post('/questions/100', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_405_incomplete_create_question_post(self):
        response = self.client().post('/questions', json=self.incomplete_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], "Method Not Allowed")

    def test_delete_question(self):
        last_question = Question.query.order_by(Question.id.desc()).first()
        test_url = '/questions/%s' % last_question.id
        
        response = self.client().delete(test_url)
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == last_question.id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_question'], last_question.id)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertIsNone(question)

    def test_delete_nonexistant_question(self):
        response = self.client().delete('/questions/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource Not Found")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()