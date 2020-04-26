import requests
files = {'upload_file': open('F://backend-flair-dectection//file.txt','rb')}
print("",files)
r = requests.post("https://flair-detection-backend.herokuapp.com/automated_testing", files=files)
print("r: ",r.text)