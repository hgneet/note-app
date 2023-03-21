from django.urls import path
from . import views

app_name = 'diary'

urlpatterns = [
    path('', views.DiaryList.as_view(), name='list'),
    path('detail/<int:pk>/', views.DiaryDetail.as_view(), name='detail'),
    path('category/<int:pk>/', views.DiaryCategoryList.as_view(), name='category'),
    path('archive/<int:year>/', views.DiaryYearList.as_view(), name='year'),
    path('archive/<int:year>/<int:month>/', views.DiaryMonthList.as_view(), name='month'),
    path('search/', views.DiarySearchList.as_view(), name='search'),
    path('note/<int:pk>/', views.DiaryNote.as_view(), name='note'),
    path('create/', views.DiaryCreateView.as_view(), name='diary_create'),
    path('create/complete/', views.DiaryCreateCompleteView.as_view(), name='diary_create_complete'),
    path('delete/<int:diary_id>/', views.DiaryDelete, name='delete'),
    path('add/', views.DiaryAdd, name='add-note'),
]