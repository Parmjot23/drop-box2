from django import forms
from .models import Document, Folder


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'folder']  # Allow optional title and folder on upload


class DocumentRenameForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']
