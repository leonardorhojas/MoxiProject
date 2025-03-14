"""
URL configuration for MoxieProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from MoxieProject.views import home
from api.views import MedspaViewSet, ServiceViewSet, AppointmentViewSet

router = DefaultRouter()
router.register(r'medspa', MedspaViewSet, basename='medspa')
router.register(r'service', ServiceViewSet, basename='service')
router.register(r'appointment', AppointmentViewSet, basename='appointment')

schema_view = get_schema_view(
    openapi.Info(
        title="Moxie Medspa API",
        default_version="v1",
        description="API documentation for Moxie Medspa's services, appointments, and medspa management",
        terms_of_service="https://www.joinmoxie.com/terms/",
        contact=openapi.Contact(email="support@joinmoxie.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', include(router.urls)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger\.json$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

]
