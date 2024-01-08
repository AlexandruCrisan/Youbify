from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, spotify_logout, process_form

urlpatterns = [
    path('spotify/get-auth-url', AuthURL.as_view()),
    path('spotify/redirect', spotify_callback),
    path('spotify/logout', spotify_logout),
    path('spotify/is-authenticated', IsAuthenticated.as_view()),
    path('process-form/', process_form, name='process_form'),
]