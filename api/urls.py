from django.urls import path
from .views import AuthURL,transfer, spotify_callback, youtube_callback, youtube_logout, spotify_logout,youtube_login, GoogleAuthRedirectView

urlpatterns = [
    path('spotify/get-auth-url', AuthURL.as_view()),
    path('spotify/redirect', spotify_callback),
    path('spotify/logout', spotify_logout),

    path('youtube/get-auth-url', GoogleAuthRedirectView.as_view()),  
    path('youtube/redirect', youtube_callback),
    path('youtube/logout', youtube_logout),
    
    path('transfer', transfer)
]