from django.conf.urls import url
from .views import GetLinksView, GetImagesView

urlpatterns = [
    url(r'^get-links/$', GetLinksView.as_view()),
    url(r'^get-images/$', GetImagesView.as_view()),
]

