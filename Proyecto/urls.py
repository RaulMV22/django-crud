
from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("singup/", views.signup, name='signup'),
    path('task/', views.task, name='task'),
    path('task_completed/', views.task_completed, name='task_completed'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('signin/', views.singin, name='inicio_sesion'),
    path('inicio/', views.vueltaInicio, name='inicio'),
    path('task/create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),

]
