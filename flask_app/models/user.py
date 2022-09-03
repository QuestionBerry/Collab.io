from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX  = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = 'collab'
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.avatar = data['avatar']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db).query_db(query, data); #returns id of new entry
    
    @classmethod
    def readOne(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def readAll(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def update(cls, data):
        query = "SET users VALUES (username=%(username)s, email=%(email)s, password=%(password)s, avatar=%(avatar)s) WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def readOneByUsername(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def readOneByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @staticmethod
    def validate(data):
        isValid = True
        if not data['username'] or not data['email'] or not data['password']:
            isValid = False
            flash("All fields are required")
        if len(data['username']) < 3:
            isValid = False
            flash("Username must be at least three characters")
        elif not User.readOneByUsername(data):
            isValid = False
            flash("Username already registered")
        if not EMAIL_REGEX.match(data['email']):
            isValid = False
            flash("Invalid Email format")
        elif not User.readOneByEmail(data):
            isValid = False
            flash("Email already registered")
        if len(data['password']) < 8:
            isValid = False
            flash("Password must be at least 8 characters")
        elif data['password'] != data['confirm']:
            isValid = False
            flash("Passwords do not match.")
        return isValid