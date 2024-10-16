import requests

url = 'https://www.skyscanner.com.my/'
r = requests.get(url)
print(r.text)