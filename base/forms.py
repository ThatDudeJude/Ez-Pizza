from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.forms import (
    TextInput,
    EmailInput,
    PasswordInput,
    CharField,
    ImageField,
    FileInput,
    widgets,
)
from django.forms import ModelForm
from .models import User


class RegisterUserForm(UserCreationForm):
    password1 = CharField(
        label="Password",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "password",
            }
        ),
    )
    password2 = CharField(
        label="Confirm Password",
        widget=PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "placeholder": "Confirm password",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["name", "username", "email"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "username": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            # 'password1': PasswordInput(attrs={
            #     'class': 'form-control',
            # })
        }


class UpdateProfileForm(ModelForm):
    # avatar = ImageField(label='Avatar',
    #         widget=)
    class Meta:
        model = User
        fields = ["avatar", "name", "username", "email"]
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "username": TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "avatar": FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }


class UpdatePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["new_password1"].widget = PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["new_password2"].widget = PasswordInput(
            attrs={"class": "form-control"}
        )


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget = EmailInput(attrs={"class": "form-control"})


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = PasswordInput(
            attrs={"class": "form-control"}
        )
        self.fields["new_password2"].widget = PasswordInput(
            attrs={"class": "form-control"}
        )
