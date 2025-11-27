# todo/urls.py

from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoListView.as_view(), name='list'),
    path('create/', views.TodoCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TodoDeleteView.as_view(), name='delete'),
    path('<int:pk>/done/', views.mark_as_done, name='mark_done'),
    path('<int:pk>/pending/', views.mark_as_pending, name='mark_pending'),
]