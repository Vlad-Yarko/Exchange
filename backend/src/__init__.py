from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from asgiref.wsgi import WsgiToAsgi

from .routers import auth, crypto, exchange
from .utils.oauth import oauth
from .config import settings


wsgi_app = Flask(__name__)

wsgi_app.secret_key = settings.SECRET_KEY

wsgi_app.register_blueprint(auth.router, url_prefix='/auth')
wsgi_app.register_blueprint(crypto.router, url_prefix='/crypto')
wsgi_app.register_blueprint(exchange.router, url_prefix='/exchange')

wsgi_app.config['SWAGGER'] = {
    'title': 'Exchange api',
    'specs_route': '/swagger'
}
Swagger(wsgi_app)

CORS(wsgi_app, supports_credentials=True, origins=['http://localhost:5173'])

oauth.init_app(wsgi_app)

asgi_app = WsgiToAsgi(wsgi_app)
