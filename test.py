import requests

base=" http://127.0.0.1:5000/add"
title={
    'title':'hello'
}
post_response=requests.post(base,data=title)