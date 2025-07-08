
from django.contrib import admin
from django.urls import path, include

import components.urls

urlpatterns = [path("admin/", admin.site.urls), 
               path("components/", include(components.urls.router.urls))]
