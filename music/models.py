from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse
from django.contrib import admin


class Album(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100)
    album_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album_logo = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.album_title + '-' + self.artist

    class Meta:
        ordering = ('artist',)


class AlbumAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Album Detail', {'fields': ('album_title', 'artist', 'genre')}),
        ('Logo', {'fields': ('album_logo',)}),
        ('User', {'fields': ('user',)}),
    ]


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    song_title = models.CharField(max_length=100)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
