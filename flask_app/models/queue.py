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
        self.artist = None
        self.client = None
        self.lastPost = None
        self.lastStatus = None
        self.response = None

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
    def readOneWithClient(cls, data):
        query = "SELECT * FROM queues LEFT JOIN users ON client_id = users.id WHERE queues.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        else:
            queue = cls(results[0])
            client_data = {
                'id' : results[0]['users.id'],
                'username' : results[0]['username'],
                'email' : results[0]['email'],
                'password' : results[0]['password'],
                'avatar' : results[0]['avatar'],
                'created_at' : results[0]['users.created_at'],
                'updated_at' : results[0]['users.updated_at']
            }
            queue.client = user.User(client_data)
            data = {
                'id' : queue.id,
                'artist_id' : queue.artist_id
            }
            queue.lastStatus = post.Post.getLastStatus(data)
            data['last_status_id'] = queue.lastStatus.id
            queue.response = post.Post.getLastResponse(data)
            return queue

    @classmethod
    def update(cls, data):
        query = "SET queues VALUES (description=%(description)s, type=%(type)s) WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM queues WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    #Pass in id of the user and get all their queues of selected type
    @classmethod
    def readAllWithUsers(cls, data):
        query = ''
        userType = data['type']
        if userType == 'client':
            query = "SELECT * FROM queues LEFT JOIN users ON client_id = users.id WHERE artist_id = %(id)s;"
        else:
            query = "SELECT * FROM queues LEFT JOIN users ON artist_id = users.id WHERE client_id = %(id)s;"

        results = connectToMySQL(cls.db).query_db(query, data)
        allQueues = []

        for row in results:
            print(userType)
            user_data = {
                'id' : row['users.id'],
                'username' : row['username'],
                'email' : row['email'],
                'password' : row['password'],
                'avatar' : row['avatar'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            queue = cls(row)
            if userType == 'client':
                queue.client = user.User(user_data)
            elif userType == 'artist':
                queue.artist = user.User(user_data)
            data = {
                'id' : queue.id,
                'artist_id' : queue.artist_id
            }
            queue.lastPost = post.Post.getLastPost(data)
            queue.lastStatus = post.Post.getLastStatus(data)
            data['last_status_id'] = queue.lastStatus.id
            queue.response = post.Post.getLastResponse(data)
            allQueues.append(queue)
        return allQueues
