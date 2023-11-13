from .models import Token
from django.utils import timezone
from datetime import timedelta
from dotenv import load_dotenv
from requests import post
import os
load_dotenv()

def get_tokens(session_id):
    user_tokens = Token.objects.filter(user=session_id)
    
    if user_tokens.exists():
        return user_tokens[0]
    return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_tokens(session_id=session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
        return
    
    tokens = Token(user=session_id, refresh_token=refresh_token, access_token=access_token, token_type=token_type, expires_in=expires_in)
    tokens.save()   
    
def is_spotify_authenticated(session_id):
    print(f"IS AUTH CHECK {session_id}")
    tokens = get_tokens(session_id=session_id)
    
    if tokens:
        expiration_date = tokens.expires_in
        
        if expiration_date <= timezone.now():
            refresh_spotify_token(tokens)
        return True
    return False    

def refresh_spotify_token(session_id):    
    refresh_token = get_tokens(session_id).refresh_token
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv("CLIENT_ID"),
        'client_secret': os.getenv("CLIENT_SECRET")
    }).json()
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')
    
    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)
    