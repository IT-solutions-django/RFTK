from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
import re
from .models import CustomUser
from invoice.models import TemplateDocument, LabelTemplateDocument


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        }),
        label="Имя пользователя"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите email'
        }),
        label="Email"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        }),
        label="Повторите пароль"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        }),
        label="Имя пользователя"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        label="Пароль"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class TemplateDocumentForm(forms.ModelForm):
    class Meta:
        model = TemplateDocument
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'id': 'editor'})
        }


class LabelTemplateForm(forms.ModelForm):
    class Meta:
        model = LabelTemplateDocument
        fields = ['label_code', 'label_desc']
        widgets = {
            'label_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Формат: {text_label}'}),
            'label_desc': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_label_code(self):
        label_code = self.cleaned_data.get('label_code')

        if not (label_code.startswith('{') and label_code.endswith('}')):
            raise forms.ValidationError("Код метки должен начинаться с '{' и заканчиваться '}'")

        inner_content = label_code[1:-1]
        if not re.match('^[a-zA-Z0-9_]+$', inner_content):
            raise forms.ValidationError("Внутри фигурных скобок должны быть только английские буквы")

        return label_code
