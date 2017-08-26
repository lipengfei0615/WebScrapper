# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Athletes(models.Model):
    athletes_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    birth_year = models.CharField(max_length=20, blank=True, null=True)
    nation = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    specials = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'athletes'


class Matchinfo(models.Model):
    info_id = models.AutoField(primary_key=True)
    meet_name = models.CharField(max_length=255, blank=True, null=True)
    meet_city = models.CharField(max_length=255, blank=True, null=True)
    entries_deadline = models.CharField(max_length=255, blank=True, null=True)
    timing = models.CharField(max_length=255, blank=True, null=True)
    organizer = models.CharField(max_length=255, blank=True, null=True)
    host_club = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matchinfo'


class Meet(models.Model):
    meets_id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    meet_name = models.CharField(max_length=255, blank=True, null=True)
    meet_type = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'meet'


class ParticipatingNation(models.Model):
    nation_id = models.AutoField(primary_key=True)
    club = models.CharField(max_length=255, blank=True, null=True)
    nation = models.CharField(max_length=255, blank=True, null=True)
    gold = models.IntegerField(blank=True, null=True)
    silver = models.IntegerField(blank=True, null=True)
    bronze = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    meet = models.ForeignKey(Meet, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'participating_nation'


class Personalbest(models.Model):
    event = models.CharField(max_length=255, blank=True, null=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    points = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    meet = models.CharField(max_length=255, blank=True, null=True)
    athletes = models.ForeignKey(Athletes, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'personalbest'


class Ranking(models.Model):
    ranking_id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=255, blank=True, null=True)
    ranking_year = models.CharField(max_length=255, blank=True, null=True)
    individuals = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    birth_year = models.CharField(max_length=255, blank=True, null=True)
    nation = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    points = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ranking'



class Recordlist(models.Model):
    recordlist = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recordlist'


class Records(models.Model):
    records_id = models.AutoField(primary_key=True)
    stroke = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    birth_year = models.CharField(max_length=255, blank=True, null=True)
    club = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    recordlist = models.ForeignKey(Recordlist, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'records'
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'