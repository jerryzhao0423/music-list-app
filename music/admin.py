from django.contrib import admin
from .models import Album, Song, AlbumAdmin


admin.site.register(Album, AlbumAdmin)
admin.site.register(Song)
