from django.contrib import admin
from .models import UploadedFile, Visualization

admin.site.register(UploadedFile)
admin.site.register(Visualization)