from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django import forms


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  ]

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data
