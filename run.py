
from flaskblog import app  # This will take from init.


# Name IS main if we run this module directly with python. It is not the case if we import this module.
if __name__ == "__main__":
    app.run(debug=True)
