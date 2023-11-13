from django.shortcuts import render, redirect
from requests import Request, post
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import update_or_create_user_tokens, is_spotify_authenticated
import os






load_dotenv()

# Create your views here.

class AuthURL(APIView):
    
    def get(self, request):
        scopes = 'playlist-read-private'
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': os.getenv("REDIRECT_URI"),
            'client_id': os.getenv("CLIENT_ID")
        }).prepare().url
    
        # return redirect(url)
        return Response({'url': url}, status=status.HTTP_200_OK)
    
def spotify_callback(request):
    print("REDIRECTED")
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv("REDIRECT_URI"),
        'client_id': os.getenv("CLIENT_ID"),
        'client_secret': os.getenv("CLIENT_SECRET")
    }).json()
    print(response)
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    
    if not request.session.session_key:
        request.session.create()
    
    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
    
    # request.session["is_authenticated"] = True
    
    # return render(request, "home.html")
    # request.session["is_authenticated"] = True
    # print(request.session["is_authenticated"])
    return redirect('base:home')
    # return render(request, "home.html")

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        # self.request.session.save()
        # if not request.session.session_key:
        #     request.session.save()
        # print(f"{request.data.get('session_key')=}")
        # print(cookies)
        # print(f"SESSION ID: {self.request.session.session_key=}")
        is_authenticated = is_spotify_authenticated(request.data.get('session_key'))
        return Response({'is_authenticated': is_authenticated}, status=status.HTTP_200_OK)
    
# AQBxToEjvloixwiaV1nGsuSVulvis9wAdbkOUUXQoIkS2Z2tPZil33yzpD2MyWbw3VneEBw1kcgypSJ-cXXIOcmSpAsz11hgZp9l3sMd15WaaencbT8NO8MR7MW4yoLcVkw