import random
from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404
from . import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from lib import subtitle
import os

# Create your views here.

#handlers
def index(request):
    context ={
        'videos': '',
        'movie_adress': '',
        'subtitle': '',
    }
    if request.user.is_authenticated:
        context['videos'] = request.user.video_set.order_by('-date')
    return render(request,'video/index.html',context)

def play_via_link(request, movie_adress):
    movie_path = request.get_full_path()[21:]
    movie_id = 'Empty'
    try:
        movie_id_index = movie_path.index('movie_id') + 9
        movie_id = movie_path[movie_id_index:]
    except:
        movie_id_index = len(movie_path) + 10
    context = {
        'videos': '',
        'movie_adress': movie_path[:movie_id_index - 10],
        'subtitle': ''
    }
    if request.user.is_authenticated:
        context['videos'] = request.user.video_set.order_by('-date')
    if movie_id != 'Empty' and get_object_or_404(models.Video, id = movie_id).subtitle != '':
        context['subtitle'] = models.Video.objects.get(id = movie_id).subtitle.url
    return render(request,'video/index.html', context)

@login_required
def add_movie(request):
    if request.method != 'POST' :
        return render(request, 'video/add_movie.html')
    context = request.POST
    video = models.Video()
    video.caption = context['caption']
    video.url = context['url']
    video.subtitle = ''
    video.user = request.user
    if 'subtitle' in request.FILES:
        video.subtitle = subtitle.storage_srt_file_as_vtt(request.FILES['subtitle'],int(random.random()*10000000000000000))
    video.save()
    return redirect('/video/')

@login_required
def delete_movie(request):
    if request.method == 'POST':
        video = get_object_or_404(models.Video, pk=request.POST['pk'])
        if video.subtitle != '':
            subtitle.remove_subtitle(video.subtitle.path)
        video.delete()
    return redirect('/video/')

@login_required
def edit_movie_page(request, movie_id):
    video = models.Video.objects.get(id = movie_id)
    return render(request, 'video/edit_movie.html', {'video': video})

@login_required
def edit_movie(request):
    if request.method == 'POST':
        print(request.POST)
        context = request.POST
        video = models.Video.objects.get(pk = context['id'])
        video.caption = context['caption']
        video.url = context['url']   
        if 'subtitle' in request.FILES:
            if video.subtitle != '':
                subtitle.remove_subtitle(video.subtitle.path)
            video.subtitle = subtitle.storage_srt_file_as_vtt(request.FILES['subtitle'],int(random.random()*10000000000000000))
        video.save()
    return redirect('/video/')

@login_required
def watch_to_gather(request):
    host = request.build_absolute_uri('/')
    url = ''
    try:
        url = models.Streamer.objects.get(user = request.user).url
    except:
        pass
    context={
        'user': request.user,
        'host': host[0:-1],
        'url':  url,
        'subtitle': '/media/' + str(request.user.id) + '.vtt',
    }
    return render(request, 'video/watch_to_gather.html', context)

def watching(request,user_id):
    url = ''
    try:
        url = models.Streamer.objects.get(user = user_id).url
    except:
        pass
    context = {
        'url': url,
        'subtitle': '/media/' + str(user_id) + '.vtt',
    }
    return render(request,'video/watching.html',context)

@login_required
def save_url(request):
    if request.method == 'POST':
        subtitle_path = os.path.join(settings.MEDIA_ROOT, str(request.user.id)+'.vtt')
        subtitle.remove_subtitle(subtitle_path)
        if 'subtitle' in request.FILES:
            subtitle.storage_srt_file_as_vtt(request.FILES['subtitle'],request.user.id)
        models.Streamer.objects.filter(user = request.user).update(url = request.POST['url'])
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(str(request.user.id),
            {
                'command': 'url',
                'url': request.POST['url'],
                'type':'receive_message',
            }
            )
    return redirect('/video/watch_to_gather')
#end handlers

