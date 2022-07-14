"""cardbase URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from cardbase import settings
from core.views import *

urlpatterns = [
    path('', CardList.as_view(), name='card_list'),
    path('card/<int:pk>', CardDetail.as_view(), name='card_detail'),
    path('card/create', card_create, name='card_create'),
    path('card/activate/<int:pk>', card_activate, name='card_activate'),
    path('card/deactivate/<int:pk>', card_deactivate, name='card_deactivate'),
    path('card/delete/<int:pk>', card_delete, name='card_delete'),

    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
