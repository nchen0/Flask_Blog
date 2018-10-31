from flaskblog import db, login_manager
from datetime import datetime  # to get current date/time.
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # Get the user with the user id
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
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
