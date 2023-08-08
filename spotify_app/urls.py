from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('index', views.index, name='index'),
                  path('search', views.search, name='search'),
                  path('', RedirectView.as_view(url='index', permanent=False)),
              ] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +
                   static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
