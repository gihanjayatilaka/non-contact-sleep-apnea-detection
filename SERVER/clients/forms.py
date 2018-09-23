from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User





class Login_Form(AuthenticationForm):

    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

    '''
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    '''

class SignUP_Form(UserCreationForm):
    #super().password1.widget=forms.PasswordInput
    #super().password2.widget=forms.PasswordInput

    email = forms.EmailField(required=True)
    email.help_text = ''

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2")

        field_classes = {'username': UsernameField}



    def save(self, commit=True):
        user = super(SignUP_Form, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user



class Register(forms.Form):


    device_id = forms.CharField()
    acess_token = forms.CharField(widget=forms.PasswordInput)







