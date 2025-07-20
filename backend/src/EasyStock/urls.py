from django.contrib import admin
from django.urls import path, include

import components.urls
import products.urls
import warehouses.urls
import supplies.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("components/", include(components.urls.router.urls)),
    path("products/", include(products.urls.router.urls)),
    path('warehouses/', include(warehouses.urls.router.urls)),
    path('supplies/', include(supplies.urls.router.urls))
]
