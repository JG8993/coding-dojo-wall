from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Post:
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator= None
    
    @classmethod
    def get_all_posts_with_creator(cls):
        query = "SELECT * FROM posts JOIN users on posts.user_id = users.id;"
        results = connectToMySQL('dojo_wall').query_db(query)
        all_posts = []
        for x in results:
            one_post = cls(x)
            one_posts_author_info = {
                "id": x['users.id'],
                "first_name":x['first_name'],
                "last_name":x['last_name'],
                "email": x['email'],
                "password":x['password'],
                "created_at":x['users.created_at'],
                "updated_at":x['users.updated_at']
            }
            author = User(one_posts_author_info)
            one_post.creator = author
            all_posts.append(one_post)
        return all_posts

    @classmethod
    def save(cls,data):
        query = "INSERT INTO posts (content,user_id) VALUES (%(content)s, %(user_id)s);"
        return connectToMySQL("dojo_wall").query_db(query,data)
        
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM posts WHERE posts.id = %(id)s;"
        return connectToMySQL("dojo_wall").query_db(query,data)
    