from django.urls import path
from .views import make_img

urlpatterns = [
    path('generate/', make_img, name='make_img'),
]