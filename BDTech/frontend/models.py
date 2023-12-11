from django.db import models

# Create your models here.
# models.py

class Equipamento(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    descricao = models.TextField()
    imagem = models.ImageField()
    preco = models.TextField()
    nome = models.TextField()

    def __str__(self):
        return self.nome  # Certifique-se de que existe um campo 'nome' no seu modelo Equipamento

    class Meta:
        db_table = 'equipamento'
""" 
class TipoEquipamento(models.Model):
    id_tipoequipamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)

class Moeda(models.Model):
    id_moeda = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100) """
