import json
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
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Acces-Control-Allow-Headers", "Content-Type,Authorization,True"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,PATCH,DELETE,OPTIONS"
        )
        return response

   

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def list_all_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)

        data = [category.format() for category in categories]
        return jsonify(
            {
            "success"    : True,
            "categories" : data,
            "totalCategories": len(categories) }
        )

    def paginate_questions(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions",  methods=["GET"])
    def shows_questions():
        questions = Question.query.order_by(Question.id).all()
        categories =[category.format() for category in Category.query.all()]

        return jsonify(
            {
              "success": True,
                "questions": paginate_questions(request, questions),
                "totalQuestions": len(questions),
                "categories": categories,
                "current_categorie": random.choice(categories)
            }
        )


   

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=['Delete'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if  question  is None:
                abort(404)
            else:
                question.delete()
                return jsonify( {
                     "success": True
                     })
        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        
        searchTerm =  body.get("searchTerm", None)
        try:
            if searchTerm:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike("%{}%".format(searchTerm)))
                current_questions = paginate_questions(request, selection)
                return jsonify({
                        "success": True,
                        "questions": current_questions,
                        "totalQuestions": len(selection.all()) } )
               
            else: 
                new_question = body.get("question", None)
                new_answer = body.get("answer", None) 
                new_category = body.get("category", None)
                new_difficulty = body.get("difficulty", None)
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category )
                question.insert()
                #selection = Question.query.order_by(Question.id).all()
                #current_questions = paginate_questions(request, selection)

                return jsonify({
                         "success" : True,
                               })
        except:
           abort(422)
            

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """



    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_question_for_category(category_id):
        try:
            questions = Question.query.order_by(Question.id).filter(Question.category == category_id)
            questions = paginate_questions(request, questions)
           
            if len(questions) == 0:
                abort(404)
            else:
                return jsonify({"success": True, "totalQuestions": len(questions), "questions": questions , "current_category":None})
                
        except:
            abort(422) 
        



    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=['POST'])
    def get_quizzes():
        
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        
        try:
                      
            new_questions = Question.query.filter_by(category = quiz_category['id']).all()
            if previous_questions and (len(new_questions) > 0):
                new_questions = [question.format() for question in new_questions]
                for question in new_questions:
                   if question['id'] in previous_questions:
                    
                        new_questions.remove(question)
                               
                question = random.choice(new_questions) 
                return jsonify({"success": True,
                                "question": question                                
                                           } )
            else: 
                abort(404)                  
       
            
        except:
            abort(422)
         


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422
        )


    @app.errorhandler(404)
    def ressource_not_found(error):
        return (
            jsonify({"succes": False, "error": 404, "message": "ressource not found"})
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request "}, 400)



    return app

