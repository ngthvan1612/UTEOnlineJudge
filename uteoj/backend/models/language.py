from django.db import models

class LanguageModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ext = models.CharField(max_length=6)
    description = models.TextField()

    def __str__(self):
        return self.name + ' (' + self.ext + ')'
