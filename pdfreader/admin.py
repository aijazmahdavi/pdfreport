from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Pdf)
class PdfAdmin(admin.ModelAdmin):
    list_display = ('pdf',)