from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

admin.site.site_header = "Friday Originals Admin"
admin.site.site_title = "Friday Originals Portal"
admin.site.index_title = "Friday Originals Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('hii.urls')),
    path('cart/', include('cart.urls')),

    path('accounts/', include('allauth.urls')),
]

# Serve media files in production
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]