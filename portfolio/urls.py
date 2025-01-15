from django.urls import path, include
from . import views
from django.urls import path
from .views import post_list, database, user_logout



urlpatterns = [
        path('', views.post_list, name="post_list"),
        path('database/',views.database, name="database"),
        path('register/', include('register.urls')),
        path('portfolio/chat/', views.chat, name="chat"),  # Update this line
        path('logout/', user_logout, name='logout'),  # Add this line to map the logout URL
        path('portfolio/analyze/', views.analyze_text, name="analyze_text"),

    ]