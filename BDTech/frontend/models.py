from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class TipoEquipamento(models.Model):
    id_tipoequipamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)

class Equipamento(models.Model):
    id_equipamento = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    imagem = models.ImageField()
    preco = models.TextField()
    id_tipoequipamento = models.ForeignKey(TipoEquipamento,null=True, on_delete=models.CASCADE, db_column='id_tipoequipamento')
 
    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'equipamento'


class Utilizador(models.Model):
    id_utilizador = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome
        
class Venda(models.Model):
    id_venda = models.AutoField(primary_key=True)
    data = models.DateField()
    valortotal = models.DecimalField(max_digits=10, decimal_places=2)
    id_utilizador = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    

class VendaEquipamento(models.Model):
    id_venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    id_equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
   