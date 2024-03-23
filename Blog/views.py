from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from .models import *
from .forms import *

# Create your views here.
def inicio(request):

    return render(request, "inicio.html", {"mensaje": "Bienvenido a Ñami"})

def contacto(request):

    return render(request, "contacto.html", {"mensaje": "Contacta con nosotros"})

def about(request):

    return render(request, "about.html", {"mensaje": "Quienes Somos?"})

def posteo(request):

    return render(request, "posteo.html", {"mensaje": "post"})

'''
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "inicio.html", {"mensaje":f"Bienvenido {username}"})
            else:
                return render(request, "inicio.html", {"mensaje":"Credenciales Incorrectas"})
    else:
        form = LoginForm()
        return render(request, 'login_usuario.html', {'form': form})

        
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, "inicio.html", {"mensaje": "El usuario ha sido creado con éxito"}) 
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})
    
'''
#### LOGIN LOGOUT REGISTRO ####
#### LOGIN LOGOUT REGISTRO ####
#### LOGIN LOGOUT REGISTRO ####

def iniciar_sesion(request):
    if request.method == "POST":
        formulario = AuthenticationForm(request, data = request.POST) #almacena la informacion que se ha puesto en el form
        if formulario.is_valid():
            info_dic = formulario.cleaned_data #convierte la info del form a un diccionario de python
            usuario = authenticate(username=info_dic["username"], password=info_dic["password"])
            if usuario is not None: #que el usuario existe!!!
                login(request, usuario)
                return render(request, "inicio.html", {"mensaje":f"Bienvenido {usuario}"})
        else:
            return render(request, "inicio.html", {"mensaje":"Credenciales Incorrectas"})
    else:
        formulario = AuthenticationForm()
    return render(request, "usuario/login_usuario.html", {"formu":formulario})

def registrarse(request):

    if request.method == "POST":
        formulario = RegistroUsuario(request.POST)
        if formulario.is_valid():
            formulario.save() #crea el nuevo usuario
            return render(request, "inicio.html", {"mensaje":"El usuario ha sido creado con éxito."})
   
    else:
        formulario = RegistroUsuario()
    return render(request, "usuario/registro.html", {"formu":formulario})

@login_required
def cerrar_sesion(request):
    logout(request)
    return render(request, "inicio.html", {"mensaje": "Sesion Cerrada con éxito"})

@login_required
def editar_usuario(request):
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Home')  # Redirigir a la página del perfil del usuario después de editar
    else:
        form = EditarUsuarioForm(instance=request.user)
    return render(request, 'usuario/editar_usuario.html', {'form': form})


### POST ###
### POST ###
### POST ###

def post_list(request):
    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user  # Asigna el usuario actual como autor del comentario
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirige al detalle de la publicación
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Asigna el usuario actual como autor del post
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def user_posts(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/user_posts.html', {'user_posts': user_posts})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Verificar que el usuario actual sea el autor de la publicación
    if request.user != post.author:
        return redirect('post_detail', pk=pk)  # Redirigir a la página de detalles de la publicación si el usuario no es el autor
    
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)  # Redirigir a la página de detalles de la publicación después de la edición
    else:
        form = PostUpdateForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('user_posts')  # Redirige a la vista de las publicaciones del usuario
    return redirect('Home')  # Redirige a otra página si no se utiliza el método POST

##ADMINISTRADORES
##ADMINISTRADORES
##ADMINISTRADORES

@login_required
def admin_dashboard(request):
    user_is_admin = check_admin_user(request.user)
    posts = Post.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'user_is_admin': user_is_admin, 'posts': posts})

def check_admin_user(user):
    administradores = Group.objects.get(name='Administradores')
    return administradores in user.groups.all()

@login_required    
def admin_edit_post(request, pk):
    if check_admin_user(request.user):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('admin_dashboard')
        else:
            form = PostUpdateForm(instance=post)
        return render(request, 'admin/admin_edit_post.html', {'form': form})
    else:
        return redirect('Home')
    
@login_required
def admin_delete_post(request, pk):
    # Verificar si el usuario actual pertenece al grupo de administradores
    if check_admin_user(request.user):
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('admin_dashboard')
    else:
        # Si el usuario no es un administrador, redirigir a otra página o mostrar un mensaje de error
        return render(request, 'inicio.html')
    

@login_required
def post_comments(request, pk):
    # Verificar si el usuario actual pertenece al grupo de administradores
    administradores = Group.objects.get(name='Administradores')
    if administradores not in request.user.groups.all():
        return render(request, 'inicio.html', {'message': 'No tienes permiso para acceder a esta página.'})

    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    return render(request, 'admin/post_comments.html', {'post': post, 'comments': comments})

@login_required
def delete_comment(request, pk):
    # Verificar si el usuario actual pertenece al grupo de administradores
    if check_admin_user(request.user):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        # Redirigir de vuelta a la página de comentarios después de eliminar el comentario
        return redirect('post_comments', pk=comment.post.pk)
    else:
        # Si el usuario no es un administrador, redirigir a otra página o mostrar un mensaje de error
        return render(request, 'inicio.html')
    

####AVATAR
####AVATAR
####AVATAR
'''    
@login_required
def agregar_avatar(request):
    if request.method == "POST":
        formulario = AvatarForm(request.POST, request.FILES)
        if formulario.is_valid():
            avatar = formulario.save(commit=False)
            avatar.usuario = request.user
            avatar.save()
            return redirect('Home')  # Redirige a la página de inicio después de agregar el avatar
    else:
        formulario = AvatarForm()
    return render(request, "avatar/nuevo_avatar.html", {"formu": formulario})


@login_required
def agregar_avatar(request):
    usuario = request.user
    try:
        avatar_existente = Avatar.objects.get(usuario=usuario)
        if request.method == "POST":
            formulario = AvatarForm(request.POST, request.FILES, instance=avatar_existente)
        else:
            formulario = AvatarForm(instance=avatar_existente)
    except Avatar.DoesNotExist:
        if request.method == "POST":
            formulario = AvatarForm(request.POST, request.FILES)
        else:
            formulario = AvatarForm()

    if request.method == "POST" and formulario.is_valid():
        nuevo_avatar = formulario.save(commit=False)
        nuevo_avatar.usuario = usuario
        nuevo_avatar.save()
        return redirect('ver_avatar')

    return render(request, 'avatar/nuevo_avatar.html', {'formulario': formulario})
'''
######ESTA FUNCIONAL
######ESTA FUNCIONAL
@login_required
def agregar_avatar(request):

    if request.method == "POST":

        formulario = AvatarForm(request.POST, request.FILES)

        if formulario.is_valid():

            info = formulario.cleaned_data

            usuario_actual = User.objects.get(username=request.user)
            nuevo_avatar = Avatar(usuario=usuario_actual, imagen=info["imagen"])

            nuevo_avatar.save()
            return render(request, "inicio.html", {"mensaje":"Has creado tu avatar"})
    
    else:

        formulario = AvatarForm()


    return render(request, "avatar/nuevo_avatar.html", {"formu":formulario})


######ESTA FUNCIONAL
######ESTA FUNCIONAL
'''  
## NUEVO - PARA SOLUCION DE MULTIPLES OBJECT - 
@login_required
def agregar_avatar(request):
    usuario_actual = request.user
    try:
        avatar_existente = Avatar.objects.get(usuario=usuario_actual)
        mensaje_confirmacion = 'Ya tienes un avatar. Puedes cargar uno nuevo si lo deseas.'
        if request.method == "POST":
            formulario = AvatarForm(request.POST, request.FILES, instance=avatar_existente)
            if formulario.is_valid():
                formulario.save()
                return redirect('ver_avatar')
        else:
            formulario = AvatarForm(instance=avatar_existente)
    except Avatar.DoesNotExist:
        mensaje_confirmacion = None
        if request.method == "POST":
            formulario = AvatarForm(request.POST, request.FILES)
            if formulario.is_valid():
                nuevo_avatar = formulario.save(commit=False)
                nuevo_avatar.usuario = usuario_actual
                nuevo_avatar.save()
                return redirect('ver_avatar')
        else:
            formulario = AvatarForm()
    return render(request, 'avatar/nuevo_avatar.html', {'formulario': formulario, 'mensaje_confirmacion': mensaje_confirmacion})

@login_required
def eliminar_avatar(request):
    usuario_actual = request.user
    avatar_actual = get_object_or_404(Avatar, usuario=usuario_actual)
    avatar_actual.delete()
    return redirect('perfil_usuario')


@login_required
def ver_avatar(request):
    avatar = get_object_or_404(Avatar, usuario=request.user)
    return render(request, "avatar/avatar.html", {"avatar": avatar})

@login_required
def avatar_no_encontrado(request):
    return render(request, "avatar/avatar_no_encontrado.html")



#####PAGINA DE EDICION DE PERFIL - VISTAS ######

@login_required
def perfil_usuario(request):
    usuario = request.user
  
    if request.method == "POST":
        # Formulario para editar los detalles del usuario
        form_perfil = EditarPerfilForm(request.POST, instance=usuario)
        # Formulario para subir o editar el avatar
        form_avatar = AvatarForm(request.POST, request.FILES, instance=avatar)

        if form_perfil.is_valid() and form_avatar.is_valid():
            form_perfil.save()
            avatar = form_avatar.save(commit=False)
            avatar.usuario = usuario
            avatar.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil_usuario')
    else:
        form_perfil = EditarPerfilForm(instance=usuario)
        form_avatar = AvatarForm(instance=avatar)

    return render(request, 'usuario/perfil_usuario.html', {'form_perfil': form_perfil, 'form_avatar': form_avatar})



   # Obtener el avatar del usuario si existe
    try:
        avatar = Avatar.objects.get(usuario=usuario)
    except Avatar.DoesNotExist:
        avatar = None
'''
