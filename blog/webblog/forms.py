from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import Movie, Comments, Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Введите пароль'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Подтвердите пароль'
    }))
    username = forms.CharField(max_length=40, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Введите имя пользователя'
    }))

    first_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Введите имя'
    }))

    last_name = forms.CharField(max_length=70, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': ' Введите фамилию'
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-light',
        'placeholder': 'Введите почту'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')


class AddMoviesForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'content', 'photo', 'video', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Введите название'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Введите описание'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light',
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select bg-dark text-light'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'style': 'resize: none; height:50px; ',
            })
        }


class EditAccountForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    old_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    new_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    confirm_password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'old_password', 'new_password', 'confirm_password')


class EditProfileForm(forms.ModelForm):
    photo = forms.FileField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))
    bio = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light'
    }))

    class Meta:
        model = Profile
        fields = ['photo', 'bio']
