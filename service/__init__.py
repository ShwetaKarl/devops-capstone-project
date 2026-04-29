"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up logging
and SQL database
"""

import sys
from flask import Flask
from flask_talisman import Talisman

from service import config
from service.common import log_handlers

# Create Flask application
app = Flask(__name__)
app.config.from_object(config)

# Enable security headers using Talisman
talisman = Talisman(app, force_https=False)
# Import routes and models
from service import routes, models  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Initialize logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("ACCOUNT SERVICE RUNNING".center(70, "*"))
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Initialize database
try:
    models.init_db(app)
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")