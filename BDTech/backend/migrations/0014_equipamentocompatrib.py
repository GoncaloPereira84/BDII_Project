# Generated by Django 4.1.13 on 2023-12-19 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_tipoequipamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipamentoCompAtrib',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_componente', models.IntegerField()),
                ('id_atributo', models.IntegerField()),
                ('id_equipamento', models.IntegerField()),
                ('valoratrib', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'equipamento_comp_atrib',
            },
        ),
    ]
