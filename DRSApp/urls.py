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
    path('profile-settings/', views.profile_settings, name='profile-settings'),
    path('manage-documents/', views.manage_documents, name='mange-documents'),
    path('view-documents/<int:id>', views.view_document, name="view-documents"),
    path('public-view-documents/<int:id>', views.public_view_document, name="public-view-documents"),
    path('update-document-status/<int:id>', views.update_upload_status, name="update-document-status"),
    path('update-upload/<int:id>', views.update_upload, name="update-upload"),
    
    path("search-documents/", views.search_documents, name="search_documents"),
    path("home-search-documents/", views.home_search_documents, name="home-search_documents"),
]
