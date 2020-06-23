import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def process_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  
  return current_questions

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
    current_questions = process_questions(request, questions)

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

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    
    # Check if question exist
    if question is None:
      abort(404)

    question.delete()
    questions = Question.query.order_by(Question.id).all()
    current_questions = process_questions(request, questions)

    return jsonify({
       'deleted_question': question_id,
       'questions': current_questions,
       'success': True,
       'total_questions': len(questions),
    })
      
  @app.route('/questions', methods=['POST'])
  def create_question():
    # Store trivia question data
    body = request.get_json()

    # Store json data if posted
    answer_key = body.get('answer', None)
    question_key = body.get('question', None)
    search_key = body.get('searchTerm', None)

    # Check if key variable is populated with post data
    if question_key:
      # Check for required field data
      if len(body['answer']) == 0 or len(body['question']) == 0:
        abort(405)
      

    try:
      # Query database using search string
      if search_key:
        search_result = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_key))).all()
        current_questions = process_questions(request, search_result)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(search_result),
          'current_category': 1,
        })

      else:
        # Create question object
        question = Question(
          question=body['question'],
          answer=body['answer'],
          category=body['category'],
          difficulty=body['difficulty']
        )

        question.insert()

        questions = Question.query.order_by(Question.id).all()
        current_questions = process_questions(request, questions)

        return jsonify({
          'created_question': question.id,
          'questions': current_questions,
          'success': True,
          'total_questions': len(questions)
        })
        
    except:
      abort(422)

  @app.route('/categories/<int:category_id>/questions')
  def get_category_questions(category_id):
    # Check for valid category id request
    categories = Category.query.all()
    if len(categories) < category_id:
      abort(404)

    # Query database and return questions by category id
    category_questions = Question.query.filter(Question.category == category_id).all()
    
    # paginate questions and format
    current_questions = process_questions(request, category_questions)

    return jsonify({
      'success': True,
      'current_category': category_id,
      'questions': current_questions,
      'total_questions': len(category_questions),
    })


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
  @app.route('/quizzes', methods=['POST'])
  def get_quiz_questjions():
    '''
    Send a post requests for a list of quiz questions based on choosen category
    '''

    # Return json object containing quiz category and previous questions list
    body = request.get_json()

    quiz_category = body.get('quiz_category')
    previous_questions = body['previous_questions']

    # Query database for questions based on selected category and store data
    category_questions = Question.query.filter(Question.category == quiz_category['id']).all()
    current_questions = [question.format() for question in category_questions]

    # randomize questions
    random.shuffle(current_questions)

    # check for and remove answered quiz questions
    for question in previous_questions:
      for item in current_questions:
        if question == item['id']:
          index = current_questions.index(item)
          current_questions.pop(index)

    # Check for empty quiz questions lists
    if len(current_questions) == 0:
      return jsonify({
        'success': True,
        'current_category': body['quiz_category']['type'],
        'question': False,
      })

    return jsonify({
      'success': True,
      'current_category': body['quiz_category']['type'],
      'question': current_questions[0]
    })

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

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': "Method Not Allowed",
    }), 405

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

    