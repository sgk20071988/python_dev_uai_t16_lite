from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8, "placeholder": "Текст поста"}),
        }
        labels = {
            "title": "Заголовок",
            "content": "Содержание",
        }