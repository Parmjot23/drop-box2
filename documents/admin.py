from django.contrib import admin
from .models import Document, Folder


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')


admin.site.register(Document, DocumentAdmin)
admin.site.register(Folder)

