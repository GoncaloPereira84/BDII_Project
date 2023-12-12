# Generated by Django 4.2.7 on 2023-12-10 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_componente_fornecedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id_estado', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.TextField()),
                ('inativo', models.BooleanField()),
            ],
            options={
                'db_table': 'estado',
                'managed': False,
            },
        ),
    ]