"""data2bots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from client.views import RegisterView
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

#  swagger docs url settings
schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Data2bots API",
        default_version='1.0.0',
        description="API documentation of Ordering App",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)  # for documentation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',
         include([
             path('', include(('client.api.urls', 'post'), namespace='orders')),
             path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
         ])
         ),

    # Authentication urls
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/register/', RegisterView.as_view(), name="register_user"),  # for registration

    path('api/user/', include('drf_user.urls')),  # for authentication except registration

]
