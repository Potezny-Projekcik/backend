# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from .managers import CustomUserManager


class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'Category'


class Director(models.Model):
    directorid = models.AutoField(primary_key=True)
    directorfirstname = models.CharField(max_length=45, blank=True, null=True)
    directorlastname = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Director'


class Directors(models.Model):
    directorsid = models.AutoField(primary_key=True)
    directorid = models.ForeignKey(Director, models.DO_NOTHING, db_column='directorid')
    movieid = models.ForeignKey('Movie', models.DO_NOTHING, db_column='movieid')

    class Meta:
        managed = False
        db_table = 'Directors'


class Language(models.Model):
    languageid = models.AutoField(primary_key=True)
    languagename = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Language'


class Languages(models.Model):
    languagesid = models.AutoField(primary_key=True)
    languageid = models.ForeignKey(Language, models.DO_NOTHING, db_column='languageid')
    movieid = models.ForeignKey('Movie', models.DO_NOTHING, db_column='movieid')

    class Meta:
        managed = False
        db_table = 'Languages'


class Movie(models.Model):
    movieid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=45)
    genre = models.CharField(max_length=45)
    countryoforigin = models.CharField(max_length=45)
    productionyear = models.DateField()
    suggestedage = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Movie'


class Moviecategory(models.Model):
    usermovieid = models.ForeignKey('Usermovies', models.DO_NOTHING, db_column='usermovieid')
    categoryid = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryid')

    class Meta:
        managed = False
        db_table = 'MovieCategory'


class Producer(models.Model):
    producerid = models.AutoField(primary_key=True)
    producername = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Producer'


class Producers(models.Model):
    producersid = models.AutoField(primary_key=True)
    producerid = models.ForeignKey(Producer, models.DO_NOTHING, db_column='producerid')
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieid')

    class Meta:
        managed = False
        db_table = 'Producers'


class User(AbstractBaseUser):

    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True, verbose_name='login')
    # login = models.CharField(max_length=64, unique=True, verbose_name='log')
    firstname = models.CharField(max_length=64, verbose_name='first name')
    lastname = models.CharField(max_length=64, verbose_name='last name')
    birthdate = models.DateField()

    isadmin = models.BooleanField()

    objects = CustomUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        managed = False
        db_table = 'User'


class Usermovies(models.Model):
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid')
    movieid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='movieid')
    usermovieid = models.AutoField(primary_key=True)
    sessiondate = models.DateField(blank=True, null=True)
    sessiontime = models.TimeField(blank=True, null=True)
    sessionpriority = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'UserMovies'
