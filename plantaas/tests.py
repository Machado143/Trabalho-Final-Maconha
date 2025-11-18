from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Planta


class PlantaModelTest(TestCase):
    """
    Testes para o model Planta do app plantaas
    """
    
    def setUp(self):
        """Configura dados de teste que serão usados em múltiplos testes"""
        self.planta_simples = Planta.objects.create(
            nome_popular="Suculenta",
            dificuldade='facil',
            necessidade_agua='baixa',
            necessidade_luz='sol_pleno'
        )
        
        self.planta_completa = Planta.objects.create(
            nome_popular="Samambaia",
            nome_cientifico="Nephrolepis exaltata",
            familia="Nephrolepidaceae",
            dificuldade='media',
            necessidade_agua='alta',
            necessidade_luz='meia_sombra',
            temperatura_minima=15,
            temperatura_maxima=30,
            descricao="Planta tropical com folhas verdes e delicadas",
            dicas_cultivo="Manter o solo sempre úmido e borrifar água nas folhas",
            toxica=False
        )
    
    def test_criacao_planta_simples(self):
        """Testa se uma planta com campos mínimos é criada corretamente"""
        self.assertEqual(self.planta_simples.nome_popular, "Suculenta")
        self.assertEqual(self.planta_simples.dificuldade, 'facil')
        self.assertIsNotNone(self.planta_simples.data_cadastro)
    
    def test_criacao_planta_completa(self):
        """Testa se uma planta com todos os campos é criada corretamente"""
        self.assertEqual(self.planta_completa.nome_popular, "Samambaia")
        self.assertEqual(self.planta_completa.nome_cientifico, "Nephrolepis exaltata")
        self.assertEqual(self.planta_completa.familia, "Nephrolepidaceae")
        self.assertEqual(self.planta_completa.temperatura_minima, 15)
        self.assertEqual(self.planta_completa.temperatura_maxima, 30)
        self.assertFalse(self.planta_completa.toxica)
    
    def test_str_method_com_nome_cientifico(self):
        """Testa o método __str__ quando a planta tem nome científico"""
        expected = "Samambaia (Nephrolepis exaltata)"
        self.assertEqual(str(self.planta_completa), expected)
    
    def test_str_method_sem_nome_cientifico(self):
        """Testa o método __str__ quando a planta não tem nome científico"""
        self.assertEqual(str(self.planta_simples), "Suculenta")
    
    def test_choices_dificuldade(self):
        """Testa se as escolhas de dificuldade funcionam corretamente"""
        self.planta_simples.dificuldade = 'dificil'
        self.planta_simples.save()
        self.assertEqual(self.planta_simples.dificuldade, 'dificil')
        self.assertEqual(self.planta_simples.get_dificuldade_display(), 'Difícil')
    
    def test_choices_necessidade_agua(self):
        """Testa se as escolhas de necessidade de água funcionam corretamente"""
        self.planta_simples.necessidade_agua = 'alta'
        self.planta_simples.save()
        self.assertEqual(self.planta_simples.necessidade_agua, 'alta')
        self.assertEqual(self.planta_simples.get_necessidade_agua_display(), 'Alta')
    
    def test_choices_necessidade_luz(self):
        """Testa se as escolhas de necessidade de luz funcionam corretamente"""
        self.planta_simples.necessidade_luz = 'sombra'
        self.planta_simples.save()
        self.assertEqual(self.planta_simples.necessidade_luz, 'sombra')
        self.assertEqual(self.planta_simples.get_necessidade_luz_display(), 'Sombra')
    
    def test_atualizacao_planta(self):
        """Testa se a atualização de uma planta funciona corretamente (UPDATE)"""
        planta = self.planta_simples
        data_anterior = planta.data_atualizacao
        
        planta.nome_popular = "Suculenta Rosa"
        planta.save()
        
        self.assertEqual(planta.nome_popular, "Suculenta Rosa")
        self.assertGreaterEqual(planta.data_atualizacao, data_anterior)
    
    def test_delecao_planta(self):
        """Testa se a exclusão de uma planta funciona corretamente (DELETE)"""
        planta_id = self.planta_simples.id
        self.planta_simples.delete()
        
        with self.assertRaises(Planta.DoesNotExist):
            Planta.objects.get(id=planta_id)
    
    def test_listagem_plantas(self):
        """Testa se a listagem de plantas retorna todas as plantas criadas (READ)"""
        plantas = Planta.objects.all()
        self.assertEqual(plantas.count(), 2)
    
    def test_ordenacao_por_nome_popular(self):
        """Testa se as plantas são ordenadas por nome popular"""
        Planta.objects.create(
            nome_popular="Zebrina",
            dificuldade='facil'
        )
        
        plantas = list(Planta.objects.all().values_list('nome_popular', flat=True))
        plantas_ordenadas = sorted(plantas)
        self.assertEqual(plantas, plantas_ordenadas)
    
    def test_validacao_temperatura(self):
        """Testa a validação de temperatura"""
        planta = Planta.objects.create(
            nome_popular="Teste",
            temperatura_minima=10,
            temperatura_maxima=25
        )
        
        # Testa temperatura válida
        planta.full_clean()  # Não deve lançar exceção
        
        # Testa temperatura inválida (muito baixa)
        planta.temperatura_minima = -20
        with self.assertRaises(ValidationError):
            planta.full_clean()
    
    def test_emoji_dificuldade(self):
        """Testa o método que retorna emoji de dificuldade"""
        self.assertEqual(self.planta_simples.get_dificuldade_display_emoji(), '🌱')
        self.assertEqual(self.planta_completa.get_dificuldade_display_emoji(), '🌿')
    
    def test_emoji_agua(self):
        """Testa o método que retorna emoji de necessidade de água"""
        self.assertEqual(self.planta_simples.get_necessidade_agua_display_emoji(), '💧')
        self.assertEqual(self.planta_completa.get_necessidade_agua_display_emoji(), '💧💧💧')
    
    def test_campo_toxica_default(self):
        """Testa se o campo tóxica tem valor padrão False"""
        planta = Planta.objects.create(nome_popular="Nova Planta")
        self.assertFalse(planta.toxica)
    
    def test_filtragem_por_dificuldade(self):
        """Testa filtragem de plantas por dificuldade"""
        plantas_faceis = Planta.objects.filter(dificuldade='facil')
        self.assertEqual(plantas_faceis.count(), 1)
        self.assertEqual(plantas_faceis.first().nome_popular, "Suculenta")