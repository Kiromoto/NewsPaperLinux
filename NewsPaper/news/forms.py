from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author',
                  'type_of_post',
                  'post_category',
                  'post_title',
                  'post_text',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('post_title')
        description = cleaned_data.get('post_text')

        if name == description:
            raise ValidationError('Заголовок и содержания новости или статьи не должны совпадать')

        return cleaned_data
