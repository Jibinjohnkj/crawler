from django.conf.urls import url
from .views import GetLinksView

urlpatterns = [
    url(r'^get-links/$', GetLinksView.as_view()),
]

