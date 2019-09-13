from django.shortcuts import render
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import Crawler

class IndexView(View):
    def get(self, request):
        """
        Show the url and depth inputs
        """
        return render(request, 'spider/index.html')

class GetLinksView(APIView):

    def post(self, request):
        url = request.data.get("url")
        depth = int(request.data.get("depth", 1))

        c = Crawler(max_depth=depth)
        c.spider(url)

        return Response({'pagesToVisit': c.pages_to_visit})