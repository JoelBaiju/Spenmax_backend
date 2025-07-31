from django.contrib import admin

# Register your models here.

from notification.models import ConfigValue

class ConfigValueAdmin(admin.ModelAdmin):
    model = ConfigValue
    model.objects = ConfigValue.objects

    def get_queryset(self, request):
        return self.model.objects.all()

admin.site.register(ConfigValue, ConfigValueAdmin)