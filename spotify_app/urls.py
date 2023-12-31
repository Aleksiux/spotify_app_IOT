from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', RedirectView.as_view(url='index', permanent=False)),
                  path('index', views.index, name='index'),
                  path('search', views.search, name='search'),
                  path('play_selected_song', views.play_selected_song, name='play_selected_song'),
                  path('play_selection', views.play_selection, name='play_selection'),
                  path('pause_selection', views.play_selection, name='pause_selection'),
                  path('music_player', views.music_player, name='music_player'),
                  path('listen_to_spotify_api', views.listenToSpotifyAPI, name='listen_to_spotify_api'),
                  path('choose_available_device', views.choose_available_device, name='choose_available_device'),
                  path('change_volume', views.change_volume, name='change_volume'),
              ] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
