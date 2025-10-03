from django.contrib import admin
from .models import RetellAgent, RetellLLM

# Register your models here.
admin.site.register(RetellAgent)
admin.site.register(RetellLLM)
