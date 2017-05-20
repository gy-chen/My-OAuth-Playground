"""Generate JWT that containes credential after OAuth login is successful.

"""
import jwt
import json
import flask
import httplib2
from flask import Blueprint
from apiclient import discovery
from oauth2client import client
from six.moves import urllib

OAUTH_STATE_PARAM_KEY_RETURN_URL = 'return_url'
JWT_SECRET = b'\xd1ue\x19\xb5\xad:]\nW\xd3\xeb\xd7\x00\xf700\xd6Z\x8d\x9d\x8bXy\x05b\x88\xa3bHh"'
JWT_PARAM_KEY_CREDENTIALS = 'credentials'

credentials_jwt = Blueprint('credentials_jwt', __name__)

@credentials_jwt.route('/')
def index():
    encoded = flask.request.args.get('jwt')
    if encoded:
        credentials = jwt.decode(encoded, key=JWT_SECRET, algorithms=['HS256'])[JWT_PARAM_KEY_CREDENTIALS]
        http_auth = client.OAuth2Credentials.from_json(credentials).authorize(httplib2.Http())
        oauth2 = discovery.build('oauth2', 'v2', http_auth)
        user = oauth2.userinfo().get().execute()
        return str(user)
    else:
        return 'Hello Jwt Login. Please go to login page.'

@credentials_jwt.route('/login')
def login():
    flow = _get_flow()
    # specific return url after get the credentials.
    param_return_url = flask.request.args.get('return_url', flask.url_for('.index', _external=True))
    state = json.dumps({ OAUTH_STATE_PARAM_KEY_RETURN_URL: param_return_url })
    auth_uri = flow.step1_get_authorize_url(state=state)
    return flask.redirect(auth_uri)

@credentials_jwt.route('/exchange_access_token')
def exchange_access_token():
    flow = _get_flow()
    if 'code' not in flask.request.args:
        return flask.redirect(flask.url_for('.login'))
    else:
        auth_code = flask.request.args.get('code')
        state_raw = flask.request.args.get('state')
        state = json.loads(state_raw)
        credentials = flow.step2_exchange(auth_code)
        # generate jwt
        return_url = state.get(PARAM_KEY_RETURN_URL, flask.url_for('.index'))
        encoded = jwt.encode({JWT_PARAM_KEY_CREDENTIALS: credentials.to_json()}, JWT_SECRET, algorithm='HS256')
        # redirect to the return url that state contains
        return_url_parsed = urllib.parse.urlparse(return_url)
        qs_dict = urllib.parse.parse_qs(return_url_parsed.query)
        qs_dict['jwt'] = encoded
        qs_str = urllib.parse.urlencode(qs_dict)
        final_return_url = urllib.parse.urljoin(return_url, '?' + qs_str)
        return flask.redirect(final_return_url)

def _get_flow():
    return client.flow_from_clientsecrets(
            'client_secret.json',
            scope='https://www.googleapis.com/auth/userinfo.profile',
            redirect_uri=flask.url_for('.exchange_access_token', _external=True))
