from rest_framework import serializers
from django.db import models

class LanguageModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ext = models.CharField(max_length=6)
    description = models.TextField()

    compile_command = models.CharField(max_length=255, blank=True)
    run_command = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name + ' (' + self.ext + ')'
