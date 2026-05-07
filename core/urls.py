from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/datasets/", include("apps.datasets.urls")),
    path("api/familles/", include("apps.datasets.urls_familles")),
    path("api/requests/", include("apps.access_requests.urls")),
    path("api/groups/", include("apps.groups.urls")),
    path("api/subscriptions/", include("apps.subscriptions.urls")),
    path("api/logs/", include("apps.logs.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)