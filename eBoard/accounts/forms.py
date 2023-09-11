from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, *args, **kwargs):
        user = super(SignUpForm, self).save(*args, **kwargs)
        announce_group = Group.objects.get(name='announce authors')
        react_group = Group.objects.get(name='react authors')
        announce_group.user_set.add(user)
        react_group.user_set.add(user)
        return user
