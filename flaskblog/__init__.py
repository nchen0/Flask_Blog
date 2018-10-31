from flask import Flask, render_template, url_for, flash, redirect
# creating an app variable, setting this as an instance of this flask. __name__ is just the name of the module. __name__ = __main__
from flask_sqlalchemy import SQLAlchemy  # this is for our database
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '529b1f33a3f14f7095089cdc1814dcbb'
# Location for our database to be. We can use sqlite here because it's the easiest to get up and running.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 3 /// to specify a relative path.

# Creating a database instance:
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)  # To initialize the bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

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
from flaskblog import routes
