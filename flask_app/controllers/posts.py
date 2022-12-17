from flask import redirect, render_template, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/create/post', methods=["POST"])
def post():
    if "user_id" not in session:
        return redirect('/')

    data = {
        "content": request.form["content"],
        "user_id": session['user_id']
    }
    Post.save(data)
    return redirect('/wall')

@app.route('/destroy/post/<int:id>') 
def delete_post(id):
    data = {
        "id": id
    }
    Post.delete(data)
    return redirect('/wall')