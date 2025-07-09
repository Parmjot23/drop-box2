from django import forms
from .models import Document, Folder, Comment


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
