from django.db import models

class LanguageModel(models.Model):
    class_name = models.CharField(max_length=128, unique=True, null=True)
    name = models.CharField(max_length=128, unique=True)
    ext = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)

    compile_command = models.CharField(max_length=255, blank=True)
    run_command = models.CharField(max_length=255, null=True)
    execute_name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.id) + '. ' + self.name + ' (' + self.ext + ')'
