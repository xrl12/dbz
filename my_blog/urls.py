from django.contrib import admin
from django.urls import path,re_path,include
from django.conf.urls.static import static
from django.conf.urls.static import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('blog.urls','blog'),namespace='blog')),

    path('ueditor/', include('DjangoUeditor.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
