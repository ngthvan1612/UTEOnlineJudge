from re import S
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, TextField
from django.db.models.fields.related import ForeignKey
from django.db.models.query_utils import check_rel_lookup_compatibility
from rest_framework import serializers


class AnnouncementModel(models.Model):
    author = ForeignKey(User, on_delete=models.CASCADE)
    title = CharField(max_length=4096)
    content = TextField()
