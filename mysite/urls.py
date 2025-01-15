
from django.contrib import admin
from django.urls import path, include
from register import views as v
from register.views import custom_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
    path('register/', include('register.urls')),
    path('login/', custom_login, name='login'),

]
