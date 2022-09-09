from sqlite3 import connect
from unittest import result
from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Post:
    db = 'collab'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.image = data['image']
        self.read = data['read']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.queue_id = data['queue_id']
        self.user_id = data['user_id']
    
    @classmethod
    def create(cls, data):
        query = "INSERT INTO posts (content, image, status, queue_id, user_id) VALUES (%(content)s, %(image)s, %(status)s, %(queue_id)s, %(user_id)s);"
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
        query = "SET posts VALUES (content=%(content)s, image=%(image)s, read=%(read)s) WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def deleteAllByQueue(cls,data):
        query = "DELETE FROM posts WHERE queue_id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getLastPost(cls, data):
        query = "SELECT * FROM posts WHERE queue_id = %(id)s ORDER BY created_at LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def getLastStatus(cls, data):
        query = "SELECT * FROM posts WHERE queue_id = %(id)s AND user_id = %(artist_id)s ORDER BY created_at;"
        results = connectToMySQL(cls.db).query_db(query, data)
        lastStatus = None
        for row in results:
            if row['status']:
                lastStatus = cls(row)
        return lastStatus

    @classmethod
    def getLastResponse(cls, data):
        query = "SELECT status FROM posts WHERE queue_id = %(id)s AND id > %(last_status_id)s AND status != '' LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return "Pending"
        else:
            return results[0]['status']
        

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