# Generated by Django 3.0.4 on 2020-04-29 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comida', '0002_auto_20200428_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hamburguesa',
            name='ingredientes',
            field=models.ManyToManyField(blank=True, to='comida.Ingrediente'),
        ),
    ]