from django.shortcuts import render
from .static.scripts import spotify_main


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
        for i in context['search_results']:
            print(i['name'])
        return render(request, 'search_result.html', context=context)
