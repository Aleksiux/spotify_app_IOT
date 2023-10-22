import json
from time import sleep

import requests
from django.shortcuts import render
from .static.scripts import spotify_main
from django.http import JsonResponse


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
        return render(request, 'music_player.html')


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


def music_player(request):
    spotify = spotify_main.SaveSongs()
    spotify.call_refresh()
    if request.method == "POST":
        action = request.POST.get('action')
        spotify = spotify_main.SaveSongs()
        spotify.call_refresh()
        if action == 'next_track':
            spotify.skip_next()
            sleep(0.3)
            context = get_playback_context(spotify)
            return render(request, 'music_player.html', context=context)
        elif action == 'prev_track':
            spotify.prev_track()
            sleep(0.3)
            context = get_playback_context(spotify)
            return render(request, 'music_player.html', context=context)
        elif action == 'pause_track':
            spotify.pause_song_on_device()
            context = get_playback_context(spotify)
            return render(request, 'music_player.html', context=context)
        elif action == 'play_track':
            spotify.play_track()
            context = get_playback_context(spotify)
            return render(request, 'music_player.html', context=context)
    try:
        context = get_playback_context(spotify)
    except TypeError:
        context = {}

    return render(request, 'music_player.html', context=context)


def choose_available_device(request):
    spotify = spotify_main.SaveSongs()
    current_device = spotify.device_id
    spotify.call_refresh()
    if request.method == 'POST':
        spotify = spotify_main.SaveSongs()
        spotify.call_refresh()
        selected_device = request.POST.get('selected_device')
        with open(
                r'C:\Users\Aleksas\PycharmProjects\spotify_api\spotify_app_IOT\spotify_app\static\scripts\devices.txt',
                'w') as f:
            f.write(selected_device)
        available_devices = spotify.get_available_devices()
        context = {
            'available_devices': available_devices,
            'current_device': current_device,
        }
        return render(request, 'choose_available_device.html', context=context)
    available_devices = spotify.get_available_devices()
    context = {
        'available_devices': available_devices,
        'current_device': current_device,
    }
    return render(request, 'choose_available_device.html', context=context)


def listenToSpotifyAPI(request):
    spotify = spotify_main.SaveSongs()
    spotify.call_refresh()
    context = get_playback_context(spotify)
    return JsonResponse(data=context)


def milliseconds_to_minutes(milliseconds):
    minutes = (milliseconds / 1000) / 60
    seconds = (milliseconds / 1000) % 60
    duration = f"{format(int(minutes), '02')}:{format(int(seconds), '02')}"
    return duration


def get_playback_context(spotify):
    playback_state = spotify.get_playback_state()
    progress = playback_state['progress_ms']
    milliseconds = playback_state['item']['duration_ms']
    duration = milliseconds_to_minutes(milliseconds)
    progress_duration = milliseconds_to_minutes(progress)
    is_currently_playing = playback_state['is_playing']
    percentage_for_progress_bar = (progress * 100) / milliseconds
    return {
        'track_name': playback_state['item']['name'],
        'artist_name': playback_state['item']['artists'][0]['name'],
        'images': playback_state['item']['album']['images'],
        'duration': duration,
        'milliseconds': milliseconds,
        'progress': progress,
        'progress_duration': progress_duration,
        'playback_state': playback_state,
        'is_currently_playing': is_currently_playing,
        'percentage': percentage_for_progress_bar,
    }


def change_volume(request):
    if request.method == "POST":
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        volume = json_data.get('volume_data')
        spotify = spotify_main.SaveSongs()
        spotify.call_refresh()
        spotify.set_playback_volume(volume)
        data = {'message': 'Volume changed successfully'}
        return JsonResponse(data)


