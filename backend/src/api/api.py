from flask import Flask, g
from flask_cors import CORS
from flasgger import Swagger
from asgiref.wsgi import WsgiToAsgi
from uvicorn import Config, Server

from .routers import subscribe, auth, crypto, currency, account, alert
from .utils.oauth import oauth
from .cors import origins
from src.config import settings
from src.databases.engine import main_session
from .responses.spam_response import SpamResponse


wsgi_app = Flask(__name__)
wsgi_app.secret_key = settings.SECRET_KEY

wsgi_app.register_blueprint(auth.router, url_prefix='/auth')
wsgi_app.register_blueprint(crypto.router, url_prefix='/crypto')
wsgi_app.register_blueprint(currency.router, url_prefix='/currency')
wsgi_app.register_blueprint(subscribe.router, url_prefix='/subscribe')
wsgi_app.register_blueprint(account.router, url_prefix='/account')
wsgi_app.register_blueprint(alert.router, url_prefix='/alert')

wsgi_app.config['SWAGGER'] = {
    'title': 'Exchange API',
    'specs_route': '/swagger'
}

Swagger(wsgi_app)

oauth.init_app(wsgi_app)

anti_spam = SpamResponse()

cors = CORS(wsgi_app, supports_credentials=True, origins=origins)


@wsgi_app.before_request
async def open_db_session():
    # response = await anti_spam.spam(request)
    # if response != 'OK':
    #     return response
    g.session = main_session()


@wsgi_app.teardown_request
async def close_db_session(exception=None):
    if 'session' in g:
        await g.session.close()
        g.pop('session', None)


asgi_app = WsgiToAsgi(wsgi_app)


async def start_api():
    server_config = Config(
        app=asgi_app
    )
    server = Server(server_config)
    await server.serve()
