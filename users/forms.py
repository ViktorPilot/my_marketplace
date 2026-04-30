from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import CustomUser

class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

class CustomCreationForm(StyleMixin, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class UserAuthenticationForm(StyleMixin, AuthenticationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['email', 'password']
