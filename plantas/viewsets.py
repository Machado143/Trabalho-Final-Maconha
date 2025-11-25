from rest_framework import viewsets
from .models import Planta
from .serializers import PlantaSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class PlantaViewSet(viewsets.ModelViewSet):
    queryset = Planta.objects.all().prefetch_related('comentarios')
    serializer_class = PlantaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)