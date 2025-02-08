from django.contrib import admin
from django.urls import path, include
from tasks.views import dashboard  # Import dashboard view

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin
    path('api/', include('tasks.urls')),  # API Endpoints
    path('', include('tasks.urls')),  # Include tasks app URLs
    path('', dashboard, name='home'),  # Homepage
]
