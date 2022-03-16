from django.urls import path
from . import views

urlpatterns = [
    # Display
    path('', views.index),
    path('wall', views.wall),

    # Action
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('post_message', views.post_message),
    path('post_comment', views.post_comment),
    path('delete_comment/<int:comment_id>', views.delete_comment),
]
