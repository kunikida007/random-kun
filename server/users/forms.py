from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()
 
 
class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        print(UserCreationForm.Meta.fields)
        fields = ("email", "username", 'password1', 'password2')


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = field.label
