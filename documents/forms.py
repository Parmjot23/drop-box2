from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']  # Allow optional title on upload


class DocumentRenameForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title']
