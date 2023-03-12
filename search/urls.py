from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginUser, name='login'),
    path('register', views.registerUser, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('list/', views.manga_list, name='manga_list'),
    path('search/', views.manga_search, name='manga_search'),
    path('details/<int:manga_id>/', views.manga_details, name='manga_details'),
    path('favorites/', views.favorite_manga, name='favorite_manga'),
    path('add_favorite_manga/', views.add_favorite_manga, name='add_favorite_manga'),
    path('remove_favorite_manga/<int:manga_id>/', views.remove_favorite_manga, name='remove_favorite_manga'),
]