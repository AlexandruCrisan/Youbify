from django.shortcuts import render, redirect
from requests import Request, post, get
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
    

        # return Response({'url': url}, status=status.HTTP_200_OK)
        return redirect(url)
    
def process_form(request):
    if request.method == 'POST':
        # Retrieve the selected choices from the form submission
        step1_choice = request.POST.get('step1_choice')
        step2_choice = request.POST.get('step2_choice')
        step3_choice = request.POST.get('step3_choice')

        # Do something with the selected choices, for example, save them to the database
        # ...

        # Redirect to a success page or return a JsonResponse
        return redirect('success_page')

    return render(request, 'home.html')  # Replace 'your_template.html' with the actual template name
    
def spotify_logout(request):
    request.session["spotify_creds"] = None
    request.session["playlists"]["spotify"] = None
    return redirect('base:home')

def get_account_name(token):
    
    response = get("https://api.spotify.com/v1/me", headers={
        "Authorization": f"Bearer {token}"
    }).json()
    # print(response.text)
    # print(response)
    return response.get('display_name')
    # return "ok"

def spotify_get_playlists(token):
    response = get("https://api.spotify.com/v1/me/playlists", headers={
        "Authorization": f"Bearer {token}"
    }).json()
    return response.get("items")
    
    
    
    
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
    
    acc_name = get_account_name(access_token)
    acc_playlists = spotify_get_playlists(access_token)
    
    # print(acc_playlists)
    
    if not request.session.session_key:
        request.session.create()
    # print(f"{request.session.session_key=}")
    
    request.session["spotify_creds"] = {
        "access_token":access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "token_type": token_type,
        "account_name": acc_name,
    }
    request.session["playlists"] = {
        "spotify": acc_playlists
    }
    
    # return render(request, 'home.html', {'spotify_playlists': acc_playlists})
    return redirect('base:home')


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