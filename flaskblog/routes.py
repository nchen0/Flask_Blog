from flask import Flask, render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

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
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}, you can log in now!', 'success')
        return redirect(url_for('login'))
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
