from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app.models import post

class Queue:
    db = 'collab'
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.type = data['type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.artist_id = data['artist_id']
        self.client_id = data['client_id']
        self.other_user = None
        self.lastPost = None
        self.lastStatus = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO queues (description, type, artist_id, client_id) VALUES (%(description)s, %(type)s, %(artist_id)s, %(client_id)s);"
        return connectToMySQL(cls.db).query_db(query, data); #returns id of new entry
    
    @classmethod
    def readOne(cls, data):
        query = "SELECT * FROM queues WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def readAll(cls):
        query = "SELECT * FROM queues;"
        results = connectToMySQL(cls.db).query_db(query)
        queues = []
        for row in results:
            queues.append(cls(row))
        return queues

    @classmethod
    def update(cls, data):
        query = "SET queues VALUES (description=%(description)s, type=%(type)s) WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM queues WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    #Pass in id of the artist and get all their clients w/ their queues
    @classmethod
    def readAllWithClients(cls, data):
        query = "SELECT * FROM queues LEFT JOIN users ON client_id = users.id WHERE artist_id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)

        allQueues = []
        for row in results:
            client_data = {
                'id' : results[0]['users.id'],
                'username' : results[0]['username'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'avatar' : results[0]['avatar'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }
            client = user.User(client_data)
            queue = cls(row)
            queue.other_user = client
            data = {
                'id' : queue.id
            }
            queue.lastPost = post.Post.getLastPost(data)
            queue.lastStatus = post.Post.getLastStatus(data)
            allQueues.append(queue)

        return allQueues




    # @staticmethod
    # def validate(data):
    #     isValid = True
    #     if len(data['description']) > 255:
    #         isValid = False
    #         flash ("Description too long")
        
    #     return isValid