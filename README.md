# andpraSDE002

## About

Authenticate user to http://www.goodreads.com website. Once the user is authenticated retrieve top 10 quotes of Mark Twain

## Prerequisites
- Use Python 3.5.0 version
- ake sure the following modules are available : bs4  , urllib.request, json. You can install these modules using pip(linux/windows) or easyinstall(windows) 


## About contents in folder ./quotes:
- This is to get top 10 Mark Twain quotes from http://www.goodreads.com website

Steps to run:
- execute command "python marktwain_quote_parser"
- this creates a file quotes.json under the same directory


## About contents in folder ./authentication:
- Currently goodreads website correctly authenticates a user but fails to redirect the user back to callback uri. To prove this I have tested ./authentication/oauth2_example.py using Google API. 

To run the above python code, do the following:
-Use Python 3.5.0 version
-Make sure the following modules are available : flask , requests_oauthlib, flask.json, os. You can install these modules using pip(linux/windows) or easyinstall(windows) 

Steps to run (to authenticate to goodreads):
- go to ./authentication
- run cmd: "python oauth2_example.py"
- the above command starts the Flask server on port 4400. 
- go to "http://localhost:4400" . This redirects to http://goodreads.com native authentication
- however, the website's redirect uri isn't working, the user will be authenticated but will not be redirected back to http://localhost:4400.


---------
| NOTES |
---------
To verify the website's redirection isn't working, comment goodreads oauth credentials and uncomment Google's in the file ./authentication/oauth2_example.py. Repeat the above steps to run to see the working example.

