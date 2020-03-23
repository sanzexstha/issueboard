from django import forms
from .models import Issue, Post
from ckeditor.widgets import CKEditorWidget


class TopicCreateForm(forms.Form):
    topic = forms.CharField(label="Subject", label_suffix="", widget=forms.TextInput(
        attrs={"class": "form-control", 'placeholder': "Enter Subject"}))
    message = forms.CharField(
        label="Message", label_suffix="", widget=CKEditorWidget())

class BoardCreateForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=False)


class PostCreateForm(forms.ModelForm):
    message = forms.CharField(
        label="Message", label_suffix="", widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['message', ]  