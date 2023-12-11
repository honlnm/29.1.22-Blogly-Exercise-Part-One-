import os
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLACHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()
    db.session.commit()

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    """shows list of all users in db"""
    users = User.query.all()
    return render_template('user-listing.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    """show new user form"""
    return render_template('new-user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """create new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/edit')
def display_user(user_id):
    """show selected user for edit"""
    user = User.query.get(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """edit selected user"""
    user = User.query.get(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')
    

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("user-detail.html", user=user)

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """delete selected user"""
    row = User.query.filter(User.id == user_id)

    row.delete()
    db.session.commit()

    return redirect("/users")

