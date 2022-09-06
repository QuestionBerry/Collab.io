from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.queue import Queue
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/queues/clients')
def client_queues():
    if 'user_id' not in session:
        return redirect('/')
    else:
        # Get all client queues, pass to render template,
        data = {
            'id' : session['user_id']
        }
        queues = Queue.readAllWithClients(data)
        return render_template('clients.html', queues=queues)

@app.route('/queues/new')
def new_queue():
    if 'user_id' not in session:
        return redirect('/')
    else:
        return render_template('new_queue.html')

@app.route('/queues/new/create', methods=['POST'])
def create_queue():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : session['user_id']
    }
    user = User.readOne(data)
    client = User.readOneByUsername(request.form)
    if not client:
        flash('Username not found')
        return redirect('/queues/new')
    elif client.id == user.id:
        flash('Cannot create queue with self')
        return redirect('/queues/new')
    else:
        queue_data = {
            'description' : request.form['description'],
            'type' : request.form['type'],
            'artist_id' : user.id,
            'client_id': client.id
        }
        newQueue = Queue.create(queue_data) 
        # Automatically create a Post after making a queue
        first_post = {
            'content' : '',
            'image_url' : '',
            'status' : 'Created',
            'queue_id' : newQueue,
            'user_id' : user.id
        }
        Post.create(first_post)
        return redirect('/queues/clients')

