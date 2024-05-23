from django.contrib import admin
from .models import Filmwork, GenreFilmwork, Genre, PersonFilmwork, Person
from django.utils.translation import gettext_lazy as _


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    verbose_name = _('filmwork_genre')
    verbose_name_plural = _('filmwork_genres')


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    verbose_name = _('filmwork_person')
    verbose_name_plural = _('filmwork_persons')
    autocomplete_fields = ('person',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

    search_fields = ('full_name', 'id')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)

    search_fields = ('name', 'description', 'id')


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline, )

    list_display = ('title', 'type', 'creation_date', 'rating',)

    list_filter = ('creation_date', 'rating', 'type',)

    search_fields = ('title', 'description', 'id')
