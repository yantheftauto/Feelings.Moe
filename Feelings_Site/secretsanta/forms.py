from django import forms

class SignupForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100),
    email = forms.EmailField(label='Email', max_length=100),
    address = forms.CharField(label='Mailing Address', max_length=200),
    interests = forms.CharField(
        label='Hobbies/Interests',
        max_length=500,
        widget=forms.Textarea(),
        required=False
    )
