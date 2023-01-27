from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import SimpleRouter

from category.views import CategoryViewSet
from hotels.views import ProductViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="Shop_api",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('account.urls')),
    path('api/v1/', include(router.urls)),

    path('api/v1/', include('hotels.urls')),

    # path('', include('posts.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)