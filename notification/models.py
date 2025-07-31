from django.db import models

class ConfigValueManager(models.Manager):
    def create(self, **kwargs):
        if self.count() >= 1:
            raise ValueError("Only one ConfigValue object can be created")
        return super().create(**kwargs)

class ConfigValue(models.Model):
    value = models.IntegerField()

    objects = ConfigValueManager()

    class Meta:
        verbose_name = 'Config Value'
        verbose_name_plural = 'Config Values'

    def save(self, *args, **kwargs):
        if ConfigValue.objects.exists() and not self.pk:
            return
        return super().save(*args, **kwargs)
