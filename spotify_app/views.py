import json

from django.shortcuts import render
from .static.scripts import spotify_main
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "index.html")


def search(request):
    if request.method == "POST":
        search_input = request.POST.get('input_search')
        spotify = spotify_main.SaveSongs()
        spotify.call_refresh()
        search_results = spotify.search_track(search_input)
        context = {
            'search_results': search_results['tracks']['items']
        }
        return render(request, 'search_result.html', context=context)


def play_selected_song(request):
    if request.method == "POST":
        selected_song = request.POST.get('selected_song')
        spotify = spotify_main.SaveSongs()
        spotify.call_refresh()
        spotify.play_song_on_device(selected_song)
        return render(request, 'playing_now.html')


def play_selection(request):
    if request.method == 'POST':
        response = json.loads(request.body)
        spotify = spotify_main.SaveSongs()
        spotify.call_refresh()
        spotify.play_song_on_device(response['selected_song'])
        context = {
        }
        return JsonResponse(context)
    return JsonResponse({'message': 'Invalid request method'})
