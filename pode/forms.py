from django import forms
from django.utils.safestring import mark_safe

from .models import UserCode


class CreateUserCodeForm(forms.Form):
    title = forms.CharField(
        label='Title',
        initial='My First HTML Page',
        max_length=40,
        required=True
    )


class EditUserCodeForm(forms.ModelForm):
    content = forms.CharField(
        label=mark_safe('<span role="heading" aria-level="2">Code</span>'),
        max_length=50000,
        required=True,
        widget=forms.Textarea
    )

    class Meta:
        model = UserCode
        fields = ['content']
