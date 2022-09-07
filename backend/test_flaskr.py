import os
from unicodedata import category
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category, username, password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(username, password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {"question": "What is the capital of Cameroon", "answer": "Yaounde", "category": 2, "difficulty":3}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """  TODO
    Write at least one test for each test for successful operation and for expected errors. """
     
    
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["categories"]))

    def test_get_questions(self):
         res = self.client().get("/questions")
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertEqual(data["success"], True)
         self.assertTrue(data["questions"])
         self.assertTrue(len(data["questions"]))
 

    def test_delete_question(self):
        res = self.client().delete("/questions/46")
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
     

    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
       
        

    def test_search_question_with_results(self):
        res = self.client().post("/questions", json={"searchTerm" : "autobiography"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(len(data["questions"]), 1)

    def test_get_quizzes(self):
        previous_questions =[2, 3, 8, 15] 
        res = self.client().post("/questions", json={"previous_questions": previous_questions,"quiz_category":"history" })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["questions"]), 4)
    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()