from django.views import generic
from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Album, Song
from .forms import UserForm, AlbumForm, SongForm


'''
class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()
'''


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


'''
class SongDetailView(generic.ListView):
    template_name = 'music/songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        return Song.objects.all()


class AlbumCreate(CreateView):
    model = Album
    fields = ['album_title', 'artist', 'genre', 'album_logo']
'''


def create_album(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {'form': form}
        return render(request, 'music/album_form.html', context)


def create_song(request, pk):
    form = SongForm(request.POST or None)
    album = get_object_or_404(Album, pk=pk)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get('song_title'):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Song existed'
                }
                return render(request, 'music/create-song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form
    }
    return render(request, 'music/create-song.html', context)


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


def delete_song(request, pk, song_id):
    album = get_object_or_404(Album, pk=pk)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'all_albums': all_albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Account is not valid'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Username/Password is not valid'})
    return render(request, 'music/login.html')


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    return render(request, 'music/login.html', {'form': form})


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        all_albums = Album.objects.filter(user=request.user)
        user = request.user
        return render(request, 'music/index.html', {'all_albums': all_albums, 'user': user})


def song_detail(request):
    if not request.user.is_authenticated:
        return render(request, 'music/login.html')
    else:
        try:
            songs_id = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    songs_id.append(song.pk)
            all_songs = Song.objects.filter(pk__in=songs_id)
            query = request.GET.get('q')
            if query:
                all_songs = all_songs.filter(
                    Q(song_title__icontains=query) |
                    Q(album__artist__icontains=query)
                ).distinct()
                return render(request, 'music/songs.html', {'all_songs': all_songs, 'q': '(contains '+query+')'})
        except Album.DoesNotExist:
            all_songs = []
        return render(request, 'music/songs.html', {'all_songs': all_songs})

