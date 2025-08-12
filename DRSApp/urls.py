from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('popup/', views.popup, name="popup"),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    
    # dashboard
    path('dash/', views.dash, name='dash'),
    path('manage-users/', views.manage_users, name='manage-users'),
    path('user-details/<int:id>/', views.user_details, name='user-details'),
]
