from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("app/",include("app.urls")),
    path("",include("app.urls")),
    path('admin/', admin.site.urls),
]
#LOAD IMAGE
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
