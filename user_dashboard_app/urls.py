from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('add_new', views.add_new),
    path('sign_in', views.sign_in),
    
    path('user_dashboard', views.user_dashboard),
    path('delete_user/<int:number>', views.delete_user, name='delete_user'),
    path('users/edit/<int:number>', views.edit_user, name='edit_user'),

    path('users/edit/', views.edit_loged_in_user),
    path('edit_information', views.edit_information),
    path('edit_loged_in_user_password', views.edit_loged_in_user_password),
    path('edit_password', views.edit_password),
    path('edit_description', views.edit_description),

    path('show/users/<int:number>', views.view_user, name='view_user'),
    path('logout', views.logout),


    path('post_message/<int:number>', views.post_message, name='post_message'),
    path('post_comment/<int:number>', views.post_comment, name= 'post_comment'),
]