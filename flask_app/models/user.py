from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask import flash

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts= []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL("dojo_wall").query_db(query,data)

    @classmethod 
    def get_all(cls,data):
        query = "SELECT * FROM users;"
        results = connectToMySQL("dojo_wall").query_db(query, data)
        user = []
        for x in results:
            user.append(cls(x))
        return user

    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("dojo_wall").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("dojo_wall").query_db(query,data)
        return cls(results[0])



    @staticmethod
    def validate(data):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("dojo_wall").query_db(query,data)
        if len(results) >=1:
            flash("Email already taken", "register")
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 chars.","register")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 chars.","register")
            is_valid = False
        if len(data['password']) < 5:
            flash("Password must be at least 5 chars.","register")
            is_valid= False
        if data['password'] != data['confirm']:
            flash("Invalid Password. Please try again.","register")
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email.","register")
            is_valid = False
        return is_valid