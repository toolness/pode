from django import forms


class CreateUserCodeForm(forms.Form):
    title = forms.CharField(
        label='Title',
        initial='My First HTML Page',
        max_length=40,
        required=True
    )
