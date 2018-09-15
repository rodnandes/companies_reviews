from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from reviews_app import views

router = DefaultRouter()
router.register(r'reviews', views.ReviewViewSet, base_name='Review')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls))
]
