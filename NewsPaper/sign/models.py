from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import pgettext_lazy


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label=pgettext_lazy("Email", "Email"))
    first_name = forms.CharField(label=pgettext_lazy("Name", "Name"))
    last_name = forms.CharField(label=pgettext_lazy("Surname", "Surname"))

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)
