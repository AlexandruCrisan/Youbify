from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, spotify_logout, process_form, youtube_login, GoogleAuthCallbackView, GoogleAuthRedirectView

urlpatterns = [
    path('spotify/get-auth-url', AuthURL.as_view()),
    path('spotify/redirect', spotify_callback),
    path('spotify/logout', spotify_logout),
    path('spotify/is-authenticated', IsAuthenticated.as_view()),
    path('process-form/', process_form, name='process_form'),
    path('youtube/prompt', GoogleAuthRedirectView.as_view()),  
    path('youtube/callback', GoogleAuthCallbackView.as_view())
]