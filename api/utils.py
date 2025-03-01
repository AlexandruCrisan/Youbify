from .models import Token
from django.utils import timezone
from datetime import timedelta
from dotenv import load_dotenv
from requests import Request, post, get
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
load_dotenv()


def get_youtube_current_channel_name(creds):
    print(creds)

    service = build(serviceName="youtube", version="v3", credentials=creds)
    response = service.channels().list(part="snippet", mine=True).execute()

    print(response)

    return response["items"][0]["snippet"]["title"]


def youtube_add_track_to_playlist(playlist_id: str, track_id: str, creds):
    service = build(serviceName="youtube", version="v3", credentials=creds)

    retry_count = 0
    max_retries = 5
    backoff_time = 1

    # In caz ca serverele de la youtube returneaza o eroare
    # se reincearca procesul de pana la 5 ori
    while retry_count < max_retries:
        try:
            response = service.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {"kind": "youtube#video", "videoId": track_id},
                    }
                },
            ).execute()
            return response
        except HttpError as err:

            if err.resp.status == 409:
                retry_count += 1
                print(
                    f"Error on playlist {playlist_id} {retry_count}/{max_retries}")
                time.sleep(backoff_time)
                backoff_time *= 2


def get_youtube_track_id(track_name, creds):
    service = build(serviceName="youtube", version="v3", credentials=creds)
    request = service.search().list(
        part="snippet",
        type="song",
        maxResults=2,
        q=track_name,
    )
    response = request.execute()
    videoid = response['items'][0]['id']['videoId']

    return videoid


def create_youtube_playlist(playlist_name: str, creds):
    service = build(serviceName="youtube", version="v3", credentials=creds)
    response = service.playlists().insert(
        part="snippet", body={"snippet": {"title": playlist_name}}
    ).execute()

    return response['id']


def get_playlist_tracks(playlist_id: str, token):
    response = get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers={
        "Authorization": f"Bearer {token}"
    }).json()

    return response["items"]


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
        tokens.save(update_fields=['access_token',
                    'refresh_token', 'expires_in', 'token_type'])
        return

    tokens = Token(user=session_id, refresh_token=refresh_token,
                   access_token=access_token, token_type=token_type, expires_in=expires_in)
    tokens.save()
