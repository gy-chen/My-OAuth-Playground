from flask import Flask
import flask
import httplib2
from apiclient import discovery
from oauth2client import client
app = Flask(__name__)
app.secret_key = b'\xfeFW\xd7\xb3\x94\xacy\xcf{\\B\x1eX\xe3Q!J\x84\x95o\xea\x90\x1f'

@app.route('/')
def hello_world():
    credentials = flask.session.get('credentials')
    user = None
    if credentials is not None:
        http_auth = client.OAuth2Credentials.from_json(credentials).authorize(httplib2.Http())
        oauth2 = discovery.build('oauth2', 'v2', http_auth)
        user = oauth2.userinfo().get().execute()
    return flask.render_template('hello.html', user=user)

@app.route('/login')
def login():
    flow = client.flow_from_clientsecrets(
        'client_secret.json',
        scope='https://www.googleapis.com/auth/userinfo.profile',
        redirect_uri=flask.url_for('login', _external=True))
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        return flask.redirect(flask.url_for('hello_world'))

@app.route('/logout')
def logout():
    flask.session.pop('credentials')
    return flask.redirect(flask.url_for('hello_world'))

@app.route('/credentials')
def credentials():
    credentials = flask.session['credentials']
    if credentials is None:
        return flask.redirect(flask.url_for('hello_world'))
    return flask.session['credentials']
