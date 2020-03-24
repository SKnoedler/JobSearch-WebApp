from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # django admin site
    path('', include('job_app.urls')) #user search site
]
