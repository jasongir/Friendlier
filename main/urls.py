from django.urls import path
from . import views
from django.conf.urls.static import static # new


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('users/<int:id>/', views.UserDetail.as_view(), name='user-detail'),
    path('post/<int:id>/', views.PostDetail.as_view(), name='post-detail'),
    path('create-post/', views.CreatePost.as_view(), name='create-post'),
    path('signup/', views.CreateUser.as_view(), name='signup'),
    path('create-comment/<int:id>/', views.CreateComment.as_view(), name="create-comment"),
]

