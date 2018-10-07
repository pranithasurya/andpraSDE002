from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import os

app = Flask(__name__)


# goodreads api credentials
client_id = "NQAaGnYgozrajGSfmafg"
client_secret = "JyX0Tf6EC7FKOheV6N93RBfdLROBgrJLBpKoV5Fkl0Q"
authorization_base_url = 'https://www.goodreads.com/oauth/authorize'
token_url = 'https://www.goodreads.com/oauth/request_token'

#google api credentials
# client_id = "941396798328-1qmijp6srvaabj8s5lf5na84kkidlgb1.apps.googleusercontent.com"
# client_secret = "zdmBGghj3CJ_h1In_vmpy5o5"
# authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
# token_url = 'https://accounts.google.com/o/oauth2/token'



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

def getdata(cmd, filename):
    os.system(cmd)
    try:
        fileloc = os.path.join(app.root_path,filename)
        print(fileloc)
        print(os.path.isfile(fileloc))
        file = open(fileloc, "r")
        if file:
            print(file.read())
        str = ""
        with open(fileloc,"r") as f:
            str+=f.read()

        return str
    except:
        print("could not find file")
        return []

@app.route('/quotes',endpoint='quotes', methods=['GET','POST', 'OPTIONS'])
def get():
    return getdata('python ../quotes/marktwain_quote_parser.py', 'quotes.json')



if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    # os.environ['DEBUG'] = "1"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.secret_key = os.urandom(24)
    app.run(port='4400')