from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.queue import Queue
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/queues/view/<int:queue_id>')
def view_queue(queue_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : queue_id
    }
    posts = Post.getAllPosts(data)
    print(queue_id)
    return render_template('view_queue.html', posts=posts, queue_id=queue_id)

@app.route('/queues/view/<int:queue_id>/post', methods=['POST'])
def new_post(queue_id):
    if 'user_id' not in session:
        return redirect('/')
    #need to make validations for post, add "" option for status
    print(request.form)
    Post.create(request.form)
    return redirect('/queues/view/' + str(queue_id))