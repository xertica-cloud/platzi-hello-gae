import os
import sys
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'lib'))
from google.appengine.ext import endpoints
from my_app.apis import SolicitudesAPI

from main import app
api = endpoints.api_server([SolicitudesAPI], restricted=False)