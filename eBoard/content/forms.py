from django import forms
from .models import Announce, UserReaction


class AnnounceForm(forms.ModelForm):
    class Meta:
        model = Announce
        fields = [
            'category',
            'title',
            'text',
        ]


class UserReactionForm(forms.ModelForm):
    class Meta:
        model = UserReaction
        fields = ('text', )
