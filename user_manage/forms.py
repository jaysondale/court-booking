from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        help_texts = {"email": "This field is required",
                      }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")