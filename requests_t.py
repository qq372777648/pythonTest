
import requests

r = requests.get('http://127.0.0.1:5000/login', auth=('lzw', '123')) # server flask:request.headers['Authorization'].
print r.text


r = requests.get('http://127.0.0.1:5000/test1', params={'token': r.text})
print r.text

