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
            'id' : session['user_id'],
            'type' : 'client'
        }
        queues = Queue.readAllWithUsers(data)
        return render_template('clients.html', queues=queues)

@app.route('/queues/orders')
def order_queues():
    if 'user_id' not in session:
        return redirect('/')
    else:
        # Get all order queues, pass to render template,
        data = {
            'id' : session['user_id'],
            'type' : 'artist'
        }
        queues = Queue.readAllWithUsers(data)
        return render_template('orders.html', queues=queues)

@app.route('/queues/new/create', methods=['POST'])
def create_queue():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : session['user_id']
    }
    user = User.readOne(data)
    client = User.readOneByUsername(request.form)
    print(client)
    if not client:
        flash('Username not found')
        return redirect('/queues/clients')
    elif client.id == user.id:
        flash('Cannot create queue with self')
        return redirect('/queues/clients')
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
            'image' : '',
            'status' : 'Created',
            'queue_id' : newQueue,
            'user_id' : user.id
        }
        Post.create(first_post)
        return redirect('/queues/clients')

@app.route('/queues/complete/<int:queue_id>')
def queue_complete(queue_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
            'content' : '',
            'image' : '',
            'status' : 'Complete',
            'queue_id' : queue_id,
            'user_id' : session['user_id']
    }
    Post.create(data)
    return redirect('/queues/clients')

@app.route('/queues/reopen/<int:queue_id>')
def queue_reopen(queue_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
            'content' : '',
            'image' : '',
            'status' : 'Reopened',
            'queue_id' : queue_id,
            'user_id' : session['user_id']
    }
    Post.create(data)
    return redirect('/queues/clients')

@app.route('/queues/delete/<int:queue_id>')
def queue_delete(queue_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : queue_id
    }
    Post.deleteAllByQueue(data)
    Queue.delete(data)
    return redirect('/queues/clients')