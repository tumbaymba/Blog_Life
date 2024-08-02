from django import forms
import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PhoneValidator:
    def __call__(self, value):
        if not re.match(r'^\d{10,13}$', value):
            raise ValidationError('Номер телефона должен содержать от 10 до 13 цифр.')


class RegisterForm(StyleFormMixin, UserCreationForm):
    """Регистрация пользователя"""

    phone = forms.CharField(max_length=20, label='Телефон',
                            widget=forms.TextInput(attrs={'placeholder': 'XXXXXXXXXXX'}),
                            validators=[PhoneValidator()])

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name', 'avatar', 'country', 'nickname',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
