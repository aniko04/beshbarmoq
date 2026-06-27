"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.views.static import serve
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('index.html', views.home, name='index'),
    
    # Auth
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('api/save-result', views.save_result, name='save_result'),
    
    # Qisqa URL lar
    path('m1', views.mashq1, name='mashq1'),
    path('m2', views.mashq2, name='mashq2'),
    path('m3', views.mashq3, name='mashq3'),
    path('m4', views.mashq4, name='mashq4'),
    path('m5', views.mashq5, name='mashq5'),
    path('m6a', views.mashq6a, name='mashq6a'),
    path('m6b', views.mashq6b, name='mashq6b'),
    path('m6c', views.mashq6c, name='mashq6c'),
    path('m7a', views.mashq7a, name='mashq7a'),
    path('m7b', views.mashq7b, name='mashq7b'),
    path('m7c', views.mashq7c, name='mashq7c'),
    path('m8a', views.mashq8a, name='mashq8a'),
    path('m8b', views.mashq8b, name='mashq8b'),
    path('m8c', views.mashq8c, name='mashq8c'),
    path('m9a', views.mashq9a, name='mashq9a'),
    path('m9a2', views.mashq9a2, name='mashq9a2'),
    path('m9b', views.mashq9b, name='mashq9b'),
    path('m9c', views.mashq9c, name='mashq9c'),
    path('m10a', views.mashq10a, name='mashq10a'),
    path('m10b', views.mashq10b, name='mashq10b'),
    path('m10c', views.mashq10c, name='mashq10c'),
    
    # Eski URL lar (backward compatibility)
    path('mashq1.html', views.mashq1, name='mashq1_html'),
    path('mashq2.html', views.mashq2, name='mashq2_html'),
    path('mashq3.html', views.mashq3, name='mashq3_html'),
    path('mashq4.html', views.mashq4, name='mashq4_html'),
    path('mashq5.html', views.mashq5, name='mashq5_html'),
    path('mashq6a.html', views.mashq6a, name='mashq6a_html'),
    path('mashq6b.html', views.mashq6b, name='mashq6b_html'),
    path('mashq6c.html', views.mashq6c, name='mashq6c_html'),
    path('mashq7a.html', views.mashq7a, name='mashq7a_html'),
    path('mashq7b.html', views.mashq7b, name='mashq7b_html'),
    path('mashq7c.html', views.mashq7c, name='mashq7c_html'),
    path('mashq8a.html', views.mashq8a, name='mashq8a_html'),
    path('mashq8b.html', views.mashq8b, name='mashq8b_html'),
    path('mashq8c.html', views.mashq8c, name='mashq8c_html'),
    path('mashq9a.html', views.mashq9a, name='mashq9a_html'),
    path('mashq9a2.html', views.mashq9a2, name='mashq9a2_html'),
    path('mashq9b.html', views.mashq9b, name='mashq9b_html'),
    path('mashq9c.html', views.mashq9c, name='mashq9c_html'),
    path('mashq10a.html', views.mashq10a, name='mashq10a_html'),
    path('mashq10b.html', views.mashq10b, name='mashq10b_html'),
    path('mashq10c.html', views.mashq10c, name='mashq10c_html'),
]

# Statikni WhiteNoise (middleware) beradi — bu yerda URL kerak emas.
# Media esa runtime'da yuklanadi, shuning uchun path() konverteri orqali beriladi.
urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
