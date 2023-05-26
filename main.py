from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'
mongo = PyMongo(app)

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired(), validators.EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', [validators.InputRequired()])
    submit = SubmitField('Sign up')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
        return render_template('index.html')

@app.route("/home")
def user():
    if 'username' in session:
        username = session['username'] = username
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route("/courses")
def courses():
    return render_template("/video/index.html")

@app.route("/notes")
def notes():
    return render_template('/notes/index.html') 

@app.route("/contact")
def contact():
    return render_template("/contact/index.html")

@app.route("/codeeditor")
def codeeditor():
    return render_template("/codeeditor/index.html")

@app.route('/blog')
def blog():
    # Fetch all the blog posts from the MongoDB database
    posts = mongo.db.blog_posts.find()
    return render_template('/blog/index.html', posts=posts) 

@app.route('/blog/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = ''
        mongo.db.blog_posts.insert_one({'title': title, 'content': content, 'image': filename})
        return redirect(url_for('blog'))
    return render_template('/blog/newpost.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/blog/<post_id>")
def show_post(post_id):
    post = mongo.db.blog_posts.find_one({'_id': ObjectId(post_id)})
    comments = mongo.db.comments.find({'post_id': post_id})
    paragraphs = post['content'].split('\n')
    return render_template("/blog/post.html", post=post, paragraphs=paragraphs, comments=comments)


@app.route('/blog/delete/<post_id>', methods=['POST'])
def delete_post(post_id):
    mongo.db.blog_posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('blog'))
@app.route('/comment', methods=['POST'])
def comment():
    # check if the user is logged in
    if 'username' not in session:
        flash('Please log in to comment.')
        return redirect(url_for('login'))

    comment_text = request.form['comment_text']
    post_id = request.form['post_id']
    username = session['username']
    
    # create a new comment document
    comment_doc = {
        'comment_text': comment_text,
        'post_id': post_id,
        'username': username
    }
    
    # insert the comment document into the comments collection
    mongo.db.comments.insert_one(comment_doc)
    
    # redirect the user back to the blog post page
    return redirect(url_for('show_post', post_id=post_id))

@app.route("/tutorials")
def tutorials():
    return render_template("/tutorials/index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            form.username.errors.append('Invalid username or password')
    return render_template('/login/index.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        existing_user = mongo.db.users.find_one({'username': username})
        if existing_user:
            form.username.errors.append('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            mongo.db.users.insert_one({'username': username, 'password': hashed_password})
            session['username'] = username
            return redirect(url_for('home'))
    return render_template('/signup/index.html', form=form)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/execute', methods=['POST'])
def execute():
    code = request.form.get('code')

    # Execute the code using subprocess
    result = subprocess.run(['python', '-c', code], capture_output=True, text=True)
    output = result.stdout.strip()

    return output

# Courses Part
@app.route('/courses/Web development Video/video1/')
def webdev1():
  return render_template('/courses/Web development Video/video1/index.html')

@app.route('/courses/Web development Video/video2/')
def webdev2():
  return render_template('/courses/Web development Video/video2/index.html')

@app.route('/courses/Web development Video/video3/')
def webdev3():
  return render_template('/courses/Web development Video/video3/index.html')

@app.route('/courses/Web development Video/video4/')
def webdev4():
  return render_template('/courses/Web development Video/video4/index.html')

@app.route('/courses/Web development Video/video5/')
def webdev5():
  return render_template('/courses/Web development Video/video5/index.html')

@app.route('/courses/Web development Video/video6/')
def webdev6():
  return render_template('/courses/Web development Video/video6/index.html')

@app.route('/courses/Web development Video/video7/')
def webdev7():
  return render_template('/courses/Web development Video/video7/index.html')

@app.route('/courses/Web development Video/video8/')
def webdev8():
  return render_template('/courses/Web development Video/video8/index.html')

@app.route('/courses/Web development Video/video9/')
def webdev9():
  return render_template('/courses/Web development Video/video9/index.html')

@app.route('/courses/Web development Video/video10/')
def webdev10():
  return render_template('/courses/Web development Video/video10/index.html')

@app.route('/courses/Web development Video/video11/')
def webdev11():
  return render_template('/courses/Web development Video/video11/index.html')

@app.route('/courses/Web development Video/project1/')
def webdevpro1():
  return render_template('/courses/Web development Video/project1/index.html')

@app.route('/courses/Web development Video/project2/')
def webdevpro2():
  return render_template('/courses/Web development Video/project2/index.html')

app.run(debug=True)