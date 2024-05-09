from django.shortcuts import render, redirect
from requests import Request, post, get
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .utils import create_youtube_playlist, get_playlist_tracks, get_youtube_track_id, youtube_add_track_to_playlist
from . import utils as ut
import os
import json
from django.views.decorators.csrf import csrf_exempt
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import time

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv()


# Create your views here.

class GoogleAuthRedirectView(APIView):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=["https://www.googleapis.com/auth/youtube"])
        flow.redirect_uri = os.getenv("YOUTUBE_REDIRECT_URI")
        authorization_url, state = flow.authorization_url(access_type='offline')
        request.session['oauth_state'] = state
        return redirect(authorization_url)

@csrf_exempt  
def transfer(request): 
    cred = Credentials(**request.session["youtube_creds"])
    data = json.loads(request.body)
    playlists_to_transfer = data.get('checked_items', [])
    
    for playlist in playlists_to_transfer:
        youtube_playlist_id = create_youtube_playlist(playlist["name"], cred)
        
        tracks = get_playlist_tracks(playlist["id"], request.session["spotify_creds"]["access_token"])
        
        [youtube_add_track_to_playlist(youtube_playlist_id, get_youtube_track_id(f'{t["track"]["name"]} {t["track"]["artists"][0]["name"]}', cred), cred) for t in tracks]
    return redirect('base:home') 


def youtube_callback(request):
    state = request.session.pop('oauth_state', None)
    if state is None or request.GET.get('state') != state:
        return redirect('login')  
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=["https://www.googleapis.com/auth/youtube"])
    
    flow.redirect_uri = os.getenv("YOUTUBE_REDIRECT_URI")
    authorization_response = request.build_absolute_uri()
    
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    if not request.session.session_key:
        request.session.create()

    request.session["youtube_creds"] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }
    
    request.session["youtube_acc_name"] = str(ut.get_youtube_current_channel_name(credentials))
    
    return redirect('base:home')


class AuthURL(APIView):
    def get(self, request):
        scopes = 'playlist-read-private'
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': os.getenv("SPOTIFY_REDIRECT_URI"),
            'client_id': os.getenv("CLIENT_ID")
        }).prepare().url

        return redirect(url)


def spotify_logout(request):
    request.session["spotify_creds"] = None
    request.session["playlists"]["spotify"] = None
    return redirect('base:home')


def youtube_logout(request):
    request.session["youtube_creds"] = None
    request.session["playlists"]["youtube"] = None
    return redirect('base:home')


def get_spotify_account_name(token):
    response = get("https://api.spotify.com/v1/me", headers={
        "Authorization": f"Bearer {token}"
    }).json()
    return response.get('display_name')


def spotify_get_playlists(token):
    response = get("https://api.spotify.com/v1/me/playlists", headers={
        "Authorization": f"Bearer {token}"
    }).json()
    return response.get("items")


def spotify_callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv("SPOTIFY_REDIRECT_URI"),
        'client_id': os.getenv("CLIENT_ID"),
        'client_secret': os.getenv("CLIENT_SECRET")
    }).json()
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    acc_name = get_spotify_account_name(access_token)
    acc_playlists = spotify_get_playlists(access_token)

    if not request.session.session_key:
        request.session.create()

    request.session["spotify_creds"] = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "token_type": token_type,
        "account_name": acc_name,
    }
    request.session["playlists"] = {
        "spotify": acc_playlists
    }
    
    return redirect('base:home')


def youtube_login(request):
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube"]
    )
    flow.run_local_server(port=1234, prompt="consent")

    credentials = flow.credentials
    print(credentials.client_secret)