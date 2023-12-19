from django.db import models

class Estado(models.Model):
    id_estado = models.AutoField(primary_key=True)
    descricao = models.TextField()
    inativo = models.BooleanField()

    def __str__(self):
        return self.descricao

    class Meta:
        managed = False
        db_table = "estado"

class Utilizador(models.Model):
    id_utilizador = models.AutoField(primary_key=True)
    nome = models.TextField()
    id_estado = models.IntegerField()
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
    tpdoc = models.CharField(max_length=255)
    ndoc = models.IntegerField()
    id_moeda = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = "venda"


class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    data = models.DateField()
    tpdoc = models.CharField(max_length = 30)
    ndoc = models.IntegerField()
    id_fornecedor = models.ForeignKey(Fornecedor, null=True, on_delete=models.CASCADE, db_column='id_fornecedor')
    id_estado = models.IntegerField()
    valortotal = models.CharField(max_length=20)
    ligaid= models.IntegerField()

    class Meta:
        managed = False
        db_table = "compra"

class Compra_Componente(models.Model):
    id_compra = models.IntegerField(primary_key=True)
    id_componente = models.IntegerField()
    quantidade = models.IntegerField()
    preco_unitario = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "compra_componente"

class TipoMaoObra(models.Model):
    id_tipomaoobra = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=255)
    custo_hora = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "tipomaoobra"

class TipoEquipamento(models.Model):
    id_tipoequipamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "tipoequipamento"