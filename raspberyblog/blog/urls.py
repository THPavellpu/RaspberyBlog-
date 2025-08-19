from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('signup/', views.signup, name='signup'), 
    path('accounts/', include('django.contrib.auth.urls')), 
]
