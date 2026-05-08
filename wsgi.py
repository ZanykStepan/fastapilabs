import sys
import os

project_home = '/home/stepanzanyk/library_app'
if project_home not in sys.path:
    sys.path.append(project_home)

from a2wsgi import ASGIMiddleware
from main import app

application = ASGIMiddleware(app)