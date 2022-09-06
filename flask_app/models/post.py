from sqlite3 import connect
from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Post:
    db = 'collab'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.image_url = data['image_url']
        self.read = data['read']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.queue_id = data['queue_id']
        self.user_id = data['user_id']
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO posts (content, image_url, status, queue_id, user_id) VALUES (%(content)s, %(image_url)s, %(status)s, %(queue_id)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data); #returns id of new entry
    
    @classmethod
    def readOne(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def update(cls, data):
        query = "SET posts VALUES (content=%(content)s, image_url=%(image_url)s, read=%(read)s) WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getLastPost(cls, data):
        query = "SELECT * FROM posts WHERE queue_id = %(id)s ORDER BY created_at LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results[0])
        return cls(results[0])

    @classmethod
    def getLastStatus(cls, data):
        query = "SELECT * FROM posts WHERE queue_id = %(id)s ORDER BY created_at;"
        results = connectToMySQL(cls.db).query_db(query, data)
        lastStatus = None
        for row in results:
            if row['status']:
                lastStatus = row['status']
        return lastStatus

    @classmethod
    def getAllPosts(cls, data):
        query = "SELECT * FROM posts WHERE queue_id = %(id)s ORDER BY created_at;"
        results = connectToMySQL(cls.db).query_db(query, data)
        allPosts = []
        for row in results:
            allPosts.append(cls(row))
        return allPosts

    @staticmethod
    def validate(data):
        isValid = True
        if data['status'] == " " or len(data['status']) < 1:
            isValid = False
            flash("Invalid status")
        return isValid