from django.db import models


class Utilizador(models.Model):
    id_utilizador = models.AutoField(primary_key=True)
    nome = models.TextField()
    id_estado = models.IntegerField(blank=True, null=True)

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


class Componente(models.Model):
    id_componente = models.AutoField(primary_key=True)
    descricao = models.TextField()
    id_estado = models.IntegerField()

    def __str__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = "componente"
