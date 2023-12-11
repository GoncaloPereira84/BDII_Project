from django.db import models
from djmoney.models.fields import MoneyField

class Utilizador(models.Model):
    id_utilizador = models.AutoField(primary_key=True)
    nome = models.TextField()
    id_estado = models.IntegerField(blank=True, null=True)
    e_cliente = models.BooleanField()

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = "utilizador"


class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    nome = models.TextField()
    id_estado = models.IntegerField()

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = "fornecedor"

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    descricao = models.TextField()
    inativo = models.BooleanField()

    def __str__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = "estado"


class Componente(models.Model):
    id_componente = models.AutoField(primary_key=True)
    id_estado = models.IntegerField()
    descricao = models.CharField(max_length=255)
    preco = models.CharField(max_length=20)
    quantidade_stock = models.IntegerField()
    imagem = models.ImageField(upload_to='imagens_componentes/')
    pcusto_medio = models.CharField(max_length=20)

    def __str__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = "componente"


class Venda(models.Model):
    id_venda = models.AutoField(primary_key=True)
    data = models.DateField()
    tpdoc = models.CharField()
    ndoc = models.IntegerField()
    id_moeda = models.CharField()

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = "venda"
