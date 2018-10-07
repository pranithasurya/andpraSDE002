from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)


# This information is obtained upon registration of a new GitHub
# client_id = "NQAaGnYgozrajGSfmafg"
# client_secret = "JyX0Tf6EC7FKOheV6N93RBfdLROBgrJLBpKoV5Fkl0Q"
# authorization_base_url = 'https://www.goodreads.com/oauth/authorize'
# token_url = 'https://www.goodreads.com/oauth/request_token'



@app.route("/")
def demo():
    """Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id, redirect_uri="http://localhost:4400/callback",scope="profile")
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    print(authorization_url)
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """
    
    github = OAuth2Session(client_id, state=session['oauth_state'],redirect_uri="http://localhost:4400/callback")
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])
    print(session['oauth_token'])
    # print(github.get('https://www.goodreads.com/api/auth_user').json())
    return "hello expedia!! Here is your access_token : " + session['oauth_token']['access_token']


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    # os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.secret_key = os.urandom(24)
    app.run(port='4400')