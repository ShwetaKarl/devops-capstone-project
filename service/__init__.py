"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

from service import routes, models  # noqa: F401 E402

from service.common import error_handlers, cli_commands  # noqa: F401 E402

log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
<<<<<<< HEAD
app.logger.info(
    "ACCOUNT SERVICE RUNNING".center(70, "*")
)
=======
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
>>>>>>> b26b91c (completed ci build5)
app.logger.info(70 * "*")

try:
    models.init_db(app)  
except Exception as error: 
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
