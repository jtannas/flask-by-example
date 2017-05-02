"""
Simple Flask application.
"""

### IMPORTS ###################################################################
import os
from flask import Flask

### APPLICATION ###############################################################
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])


### VIEWS #####################################################################
@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


### RUN MAIN ##################################################################
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
