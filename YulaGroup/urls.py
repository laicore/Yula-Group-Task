"""YulaGroup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from newsnetwork import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',views.signup),
    path('logout/',views.logout),
    path('login/',views.login),
    path('',views.main),    
    path('addpost/',views.addNews),
    path('post/<int:id>/',views.postshow),
    path('profile/',views.profile),
    path('loadNews/',views.loadNews)
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)