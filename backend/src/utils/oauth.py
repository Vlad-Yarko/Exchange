from authlib.integrations.flask_client import OAuth
from ..config import settings


oauth = OAuth()
# google = oauth.register(
#     name='google',
#     client_id=settings.CLIENT_ID,
#     client_secret=settings.CLIENT_SECRET,
#     server_metadata_uri='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid profile email'},
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     redirect_uri='http://localhost:8000/auth/authorize/google',
#     access_token_url='https://oauth2.googleapis.com/token'
# )

google = oauth.register(
    name="google",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    access_token_url="https://www.googleapis.com/oauth2/v4/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v3/",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)
