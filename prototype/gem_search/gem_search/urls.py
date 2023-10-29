from django.contrib import admin
from django.urls import path, include
from searchapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search, name='search'),
]
