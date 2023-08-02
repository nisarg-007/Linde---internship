from django.contrib import admin

# Register your models here.
from .models import Suggestion_Data
admin.site.register(Suggestion_Data)

from .models import Login
admin.site.register(Login)