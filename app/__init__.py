from flask import Flask

# initialize a Flask object named app
app = Flask(__name__)

# Defines what will happen if the user goes to '/' endpoint
@app.route('/')
def index():
    return "I'm having so much fun learning wed dev"