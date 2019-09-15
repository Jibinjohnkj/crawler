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

    def get(self, request):
        url = request.query_params.get("url")
        depth = int(request.query_params.get("depth", 1))

        c = Crawler(url, max_depth=depth)
        return Response({'links': c.get_links()})

class GetImagesView(APIView):

    def get(self, request):
        url = request.query_params.get("url")
        c = Crawler(url)

        # Remove duplicates
        images = set(c.get_images())
        return Response({'images': images, 'url': url})