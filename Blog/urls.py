from django.urls import path
from .views import *

urlpatterns = [
        path("about/", about, name= "About"),
        path("contacto/", contacto, name= "contacto"),

        path('login/', iniciar_sesion, name='login_usuario'),
        path('logout/', cerrar_sesion, name='logout_usuario'),
        path('editar_usuario/', editar_usuario, name='editar_usuario'),
        path('perfil/', editar_usuario, name='perfil_usuario'),
        path('registro/', registrarse, name='registro'),

        path("post_list/", post_list, name= "post_list"),
        path("post/<int:pk>/", post_detail, name= "post_detail"),
        path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
        path('post/create/', create_post, name='create_post'),
        path('user_posts/', user_posts, name='user_posts'),
        path('delete_post/<int:pk>/', delete_post, name='delete_post'),
        path('post/<int:pk>/edit/', edit_post, name='edit_post'),
        path("publi/", posteo, name= "posteo"),

        path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
        path('admin/edit_post/<int:pk>/', admin_edit_post, name='admin_edit_post'),
        path('admin/delete_post/<int:pk>/', admin_delete_post, name='admin_delete_post'),
        path('post_comments/<int:pk>/', post_comments, name='post_comments'),
        path('delete_comment/<int:pk>/', delete_comment, name='delete_comment'),

        path('agregar_avatar/', agregar_avatar, name='agregar_avatar'),
       # path('avatar/', ver_avatar, name='ver_avatar'),
        #path('avatar_no_encontrado/', avatar_no_encontrado, name='avatar_no_encontrado'),
        #path('eliminar_avatar/', eliminar_avatar, name='eliminar_avatar'),


        path('', inicio, name='Home'),

        
]