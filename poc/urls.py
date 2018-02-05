from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('display-results.html', views.displayResults, name='displayResults'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)