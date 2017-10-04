from urllib.parse import urlencode
import webbrowser
import webserver

# Based on instructions from:
# https://developers.google.com/identity/protocols/OAuth2InstalledApp

client_id = "1025187389465-0kg6h5m0ht2tlkassjpadmlv3gkg5keu.apps.googleusercontent.com"

def startAuth():
	# Step 0: Start local web server to complete oauth
	print("Starting web server")
	webserver.startBackground()

	# Step 1: Create Code Verifier

	# Step 2: Send request to google's oauth2 server
	params = {
		"client_id": client_id,
		"redirect_uri": "http://localhost:8453/auth/native/token",
		"response_type": "code",
		"scope": "openid profile"
	}
	url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

	# Open url with user's browser
	print("Opening browser")
	webbrowser.open(url)
