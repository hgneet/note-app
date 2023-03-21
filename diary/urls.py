from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.DiaryList.as_view(), name='list'),
    path('detail/<int:pk>/', views.DiaryDetail.as_view(), name='detail'),
    path('delete/<int:diary_id>/', views.DiaryDelete, name='delete'),
    path('add/', views.DiaryAdd, name='add-note'),
]