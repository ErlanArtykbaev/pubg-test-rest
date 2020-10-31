from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import RatesCreateSerializer
from .models import Rates


class RatesView(ListCreateAPIView):
    queryset = Rates.objects.all()
    serializer_class = RatesCreateSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(Rates, id=self.request.data.get('author_id'))
        return serializer.save(author=author)


class RatesSingleView(RetrieveUpdateDestroyAPIView):
    queryset = Rates.objects.all()
    serializer_class = RatesCreateSerializer


# Create your views here.