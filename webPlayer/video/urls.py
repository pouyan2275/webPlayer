from django.urls import path
from . import views

app_name = 'video'

urlpatterns = [
    path('', views.index, name='home'),
    path('play_via_link/<path:movie_adress>', views.play_via_link, name='play_via_link'),
    path('add_movie/', views.add_movie, name="add_movie"),
    path('delete_movie/', views.delete_movie, name="delete_movie"),
    path('edit_movie_page/<int:movie_id>/', views.edit_movie_page, name='edit_movie_page'),
    path('edit_movie/', views.edit_movie, name='edit_movie'),
    path('watch_to_gather', views.watch_to_gather, name='watch_to_gather'),
    path('watching/<int:user_id>', views.watching, name="watching"),
    path('save_url',views.save_url, name="save_url"),
]
