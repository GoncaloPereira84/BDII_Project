from django.db import models

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

class Fornecedor(models.Model):
    id_fornecedor = models.AutoField(primary_key=True)
    id_estado = models.IntegerField()
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    codpostal = models.CharField(max_length=10)
    localidade = models.CharField(max_length=255)
    contacto = models.CharField(max_length=20)
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = "fornecedor"