from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Equipamento(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    nome = models.CharField()
    descricao = models.TextField()
    imagem = models.ImageField()
    preco = models.TextField()

    def __str__(self):
        return self.nome

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
