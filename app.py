"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()


@app.route("/")
def show_homepage():
    """ Redirects to list of users. """

    return redirect ("/users")


@app.route("/users")
def show_user_list(): 
    """ Shows list of all users. """

    users = User.query.all()

    return render_template("user_listing.html", users=users)


@app.route("/users/new")
def show_add_user_form(): 
    """ Shows form to add new user. """

    return render_template ("new_user.html")


@app.route("/users/new", methods=["POST"])
def add_user(): 
    """ Creates new user from input """

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['img-url'] or None

    user = User(
                first_name=first_name,
                last_name=last_name,
                image_url=image_url
                )

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id): 
    """ Show info on a single user. """

    user = User.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_page(user_id): 
    """ Shows edit page. """

    user = User.query.get_or_404(user_id)
    return render_template("user_edit_page.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id): 
    """ Allows user to edit profile. """

    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url'] or None

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id): 
    """ Allows user to delete profile. """
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


