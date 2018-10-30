from datetime import datetime  # to get current date/time.
from flask import Flask, render_template, url_for, flash, redirect
# creating an app variable, setting this as an instance of this flask. __name__ is just the name of the module. __name__ = __main__
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy  # this is for our database


app = Flask(__name__)

app.config['SECRET_KEY'] = '529b1f33a3f14f7095089cdc1814dcbb'
# Location for our database to be. We can use sqlite here because it's the easiest to get up and running.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 3 /// to specify a relative path.

# Creating a database instance:
db = SQLAlchemy(app)
# start with: from flaskblog import db
# use db.create_all() in python terminal to add the site.db that we created above.

# To create the user instance: from flaskblog import User, Post:
# user_1 = User('pass in user fields here')
# db.session.add(user_1)
# To commit the changes:
# db.session.commit()

# Then: we can search the database like this:
# User.query.all() or: User.query.first()
# User.query.filter_by(username="Nicky").all()
# To clear the database: db.drop_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # 20 notates a 20 max char limit.
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # for the user's profile picture. We'll hash the image files.
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    # We're saying our post attribute has a relationship to the post model. The backref is similar to adding another column to the Post model. When we have a post, we can use this author attribute to get the author who created the post. The lazy defines when sql alchemy loads the database. True is when sqlalchemy will load the database in one go. WIth this, we can get all the posts made by a specific user. If we're to look at our database structure, we won't see the post column here, it is simply just a query in the background the user has created.

    # This is how our object printed whenever we print it out, this is the same as __str__.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # This is how our object printed whenever we print it out, this is the same as __str__.
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    # Post and user model has a relationship because users author posts. This will be a one to many relationship because one author can make many posts but a post can only have one author.


posts = [
    {
        'author': 'Nick C',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Oct 20, 2018'
    },
    {
        'author': 'Jane D',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Oct 27, 2018'
    }
]


# This is how you create a route in the simplest form. We create routes using decorators in flask.
# / is the home page of our website. Normally we want to return HTML, but we'll start with just hello world.
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


# To run:
"""
- set FLASK_APP=flaskblog.py
- flask run

To turn on auto update (and not have to restart the server each time):
- set FLASK_DEBUG=1
- flask run

Another way:
- if __name__ == "__main__":
    app.run(debug=True)
- python flaskblog.py
"""


@app.route("/about")
def about():
    return render_template('about.html', title="About")  # "<h1>About Page</h1>"  # We could return all of our html things here with ''' ''', but with a lot of pages and routes, this would become really ugly and unwieldy. The best way would be to use templates.


# If we ever want multiple routes handled by the same function, it's as simple as adding another decorator.
# like /home.

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # will tell us if the form validated when submitted. We can use a flash message for this.
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful, Please check username and password', 'danger')
    return render_template('login.html', title="Login", form=form)


# Name IS main if we run this module directly with python. It is not the case if we import this module.
if __name__ == "__main__":
    app.run(debug=True)
