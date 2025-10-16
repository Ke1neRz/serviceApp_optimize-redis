from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.db import router
from rest_framework import routers

from service import settings
from services.views import SubscriptionView


urlpatterns = [
    path('admin/', admin.site.urls),
]

router = routers.DefaultRouter()
router.register(r'api/subscriptions', SubscriptionView)

urlpatterns += router.urls

if settings.DEBUG:
    # urlpatterns += [
    #     path("__debug__/", include("debug_toolbar.urls")),
    # ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
