from flask import Flask,redirect,request
import threading

app = Flask(__name__)

@app.route("/")
def home():
	return redirect("https://baseline.ws/")

@app.route("/auth/native/token")
def auth():
	code = request.args.get("code")
	if code is not None:
		print("Received oauth callback " + code)
		return "Authentication successful, please close this tab"
	else:
		return "Authentication failed"

# Start local webserver
def start():
	app.run(port=8453)

def startBackground():
	server_thread = threading.Thread(target=start)
	server_thread.start()
