from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
    path('category/<int:pk>/', MovieListByCategory.as_view(), name='category'),
    path('movie//<int:pk>/', MoviesDetailView.as_view(), name='movie'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register_view, name='register'),
    path('add_movies/', AddMovie.as_view(), name='add_movies'),
    path('movie/<int:pk>/update/', MovieUpdate.as_view(), name='update'),
    path('movie/<int:pk>/delete/', DeleteMovie.as_view(), name='delete'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('update_comment/<int:pk>/update_comment', CommentUpdate.as_view(), name='comment_update'),
    path('delete_comment/<int:pk>/', comment_delete, name='delete_comment'),
    path('search/', SearchResults.as_view(), name='search'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('edit_account/', edit_account_view, name='edit_account'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
]
