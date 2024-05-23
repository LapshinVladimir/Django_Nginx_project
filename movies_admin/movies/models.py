from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey(
        'Person', verbose_name=_('Person'), on_delete=models.CASCADE)

    class FilmRole(models.TextChoices):
        DIRECTOR = 'director', _('Director')
        ACTOR = 'actor', _('Actor')
        PRODUCER = 'producer', _('Producer')
        OPERATOR = 'operator', _('Operator')

    role = models.TextField(_('role'), choices=FilmRole.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    obj_name = str(_('Person'))

    def __str__(self):
        return self.obj_name

    class Meta:
        db_table = "content\".\"person_film_work"
        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_idx')
        ]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full name'), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Star')
        verbose_name_plural = _('Stars')


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        'Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey(
        'Genre', verbose_name=_('Genre'), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    obj_name = str(_('Genre'))

    def __str__(self):
        return self.obj_name

    class Meta:
        db_table = "content\".\"genre_film_work"
        constraints = [
            models.UniqueConstraint(fields=['film_work', 'genre'],
                                    name='film_work_genre_idx')
        ]


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')


class Filmwork(UUIDMixin, TimeStampedMixin):
    certificate = models.CharField(_('certificate'),
                                   null=True, max_length=512, blank=True)
    title = models.CharField(_('name'), max_length=255)
    file_path = models.FileField(_('file'),
                                 blank=True, null=True, upload_to='movies/')
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_("creation_date"),)
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])

    class FilmType(models.TextChoices):
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')

    type = models.TextField(_('type'), choices=FilmType.choices, null=True)

    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(
                fields=['title'],
                name='film_work_title_idx'),
            models.Index(
                fields=['creation_date'],
                name='film_work_creation_date_idx'),
        ]
        db_table = "content\".\"film_work"
        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')
