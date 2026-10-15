from django.conf import settings
from django.contrib import admin
from django.urls import include, path
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]