"""
This module is part of implementing Flask-Script.

The Flask-Script extension provides support for writing external
scripts in Flask. This includes running a development server, a
customised Python shell, scripts to set up your database, cronjobs, and
other command-line tasks that belong outside the web application itself.
"""
### IMPORTS ###################################################################
import os
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

### CONFIG THE APP AND REGISTER EXTENSIONS ####################################
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)

### COMMANDS ##################################################################
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=8080))

### RUN MAIN ##################################################################
if __name__ == '__main__':
    manager.run()
