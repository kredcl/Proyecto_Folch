from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *

class RegistroForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistroUsuario(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name",  "email", "password1", "password2"]

class EditarUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

###POST
###POST
###POST

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  # Puedes quitar 'image' si no deseas que se agregue una imagen al crear una publicación

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']

## EDITAR PERFIL PARA NUEVA PAGINA DE EDICIONDEPERFIL

class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


'''
class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ['imagen']
        labels = {'imagen': 'Avatar'}
        help_texts = {'imagen': 'Ya tienes un avatar. Puedes cargar uno nuevo si lo deseas.'}
'''
