from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser
from django import forms


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'phone_number':
                self.fields[field].widget.attrs.update({"class": "form-control"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": "X-XXX-XXX-XX-XX"})


class CustomCreationForm(StyleMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class UserAuthenticationForm(StyleMixin, AuthenticationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'password']

class UserModelForm(StyleMixin, forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'avatar', 'phone_number', 'country']
