import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  # CORS(app, resources={r"*/api/*": {"origins": '*'}})
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories')
  def get_categories():
    # Query category data and return as json payload
    categories = Category.query.all()

    # Return 404 if query returns no data
    if not categories:
      abort(404)
    
    formatted_categories = {category.id: category.type for category in categories}
    
    return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(categories)
    })

  @app.route('/questions')
  def get_paginated_questions():
    # Query question data and paginate/format
    page = request.args.get('page', 1, type=int)

    # Default to page 1 if query argument is 0 or less than 0
    if page <= 0:
      page = 1
    
    # Query questions table and format return
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    start = (page - 1) * 10
    end = start + 10
    current_questions = formatted_questions[start:end]

    # Return 404 if page query is invalid value
    if not current_questions:
      abort(404)

    # Query category data and format
    categories = Category.query.all()
    formatted_categories = {category.id: category.type for category in categories}

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formatted_categories,
      'current_category': None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      
      # Check if question exist
      if question is None:
        abort(404)

      question.delete()
      questions = Question.query.order_by(Question.id).all()
      formatted_questions = [question.format() for question in questions]

      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + 10

      current_questions = formatted_questions[start:end]

      return jsonify({
        'deleted_question': question_id,
        'questions': current_questions,
        'success': True,
        'total_question': len(questions),
      })
    
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
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

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


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

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': "Resource Not Found",
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': "Unprocessable",
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': "Internal Server Error",
    }), 500
  
  return app

    