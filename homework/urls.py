from django.urls import path
from . import views


urlpatterns = [
  

    # Teacher URLS  
    path('create_homework/', views.create_homework, name='create_homework'),  # Teacher creates homework
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  # Child's dashboard
    path('homework/<int:pk>/', views.homework_detail, name='homework_detail'),
    path('add-child/', views.create_child_view, name='create_child'),
   
#     #Child URLs
    path('child_dashboard/', views.child_dashboard, name='child_dashboard'),
    path('child_dashboard/<int:hw_id>/', views.child_dashboard, name='child_dashboard'),
    path('child_game_page/', views.child_game_page,name='child_game_page'),
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),
   
#     #Parent URLs
#     path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),  # Parent's dashboard
   
 ]

