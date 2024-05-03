# Generated by Django 5.0.4 on 2024-05-03 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lib_sys', '0014_remove_livre_pret_livre_statut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livre',
            name='statut',
            field=models.CharField(choices=[('Disponible pour prêt', 'Disponible'), ('Hors prêt', 'Hors prêt')], default='Disponible pour prêt', max_length=50),
        ),
    ]