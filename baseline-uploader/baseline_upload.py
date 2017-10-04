import requests

def upload(authToken, trackFile):
	# POST to baseline web server
	url = "https://baseline.ws/tracks"
	headers = {
		"User-Agent": "BASEline Native Uploader/1.0",
		"Authorization": authToken
	}
	data = open(trackFile, "rb").read()
	result = requests.post(url, headers=headers, data=data)
	return result.status_code == 200
