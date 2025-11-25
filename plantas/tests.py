from django.test import TestCase
from django.contrib.auth.models import User
from .models import Planta

class PlantaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha123')
        self.planta = Planta.objects.create(
            nome="Samambaia",
            especie="Nephrolepis exaltata",
            dificuldade='F',
            necessidade_agua="Moderada",
            necessidade_luz="Sombra parcial",
            descricao="Planta perene",
            autor=self.user
        )
    
    def test_planta_str(self):
        self.assertEqual(str(self.planta), "SAMAMBIA (Nephrolepis exaltata)")
    
    def test_total_dicas(self):
        self.assertEqual(self.planta.total_dicas(), 0)