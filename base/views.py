from django.http import HttpResponse
from django.shortcuts import render
from requests import get
import requests
import axios

# Create your views here.
def home(request):
    if not request.session.session_key:
        request.session.create()
    # cookies = {"session_key": request.session.session_key}
    # session = request.session
    # response = get('http://127.0.0.1:8000/api/is-authenticated', data=cookies).json()
    # print(response)
    # print(f"{request.session.session_key=}")
    # request.session["is_authenticated"] = response.get("is_authenticated")
    # request.session["is_authenticated"] = False
    
    return render(request, "home.html")

def sample(request):
    return render(request, "test.html")