import os
from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.queue import Queue
from flask_app.models.user import User
from flask_app.models.post import Post
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route('/queues/view/<int:queue_id>')
def view_queue(queue_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : queue_id
    }
    posts = Post.getAllPosts(data)
    queue = Queue.readOneWithClient(data)
    return render_template('view_queue.html', posts=posts, queue=queue)

@app.route('/queues/view/<int:queue_id>/post', methods=['POST'])
def new_post(queue_id):
    if 'user_id' not in session:
        return redirect('/')

    file = request.files['file']
    print(file)
    data = {
        'content' : request.form['content'],
        'status' : request.form['status'],
        'image' : '',
        'queue_id' : queue_id,
        'user_id' : request.form['user_id']
    }
    if data['content'] == '' and data['status'] == '':
        flash('Make a comment, change a status or upload an image to post.')
        return redirect('/queues/view/' + str(queue_id))

    if file and file.filename != '':
        if not allowed_file(file.filename):
            flash('Allowed image types are .png .jpg .jpeg .gif')
            return redirect('/queues/view/' + str(queue_id))
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        data['image'] = filename
    
    print(Post.create(data))
    return redirect('/queues/view/' + str(queue_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


