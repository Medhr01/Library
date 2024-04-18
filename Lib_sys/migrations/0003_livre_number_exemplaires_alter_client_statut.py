# Generated by Django 5.0.4 on 2024-04-08 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Lib_sys', '0002_client_exemplaire_livre_remove_muser_age_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livre',
            name='number_exemplaires',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='statut',
            field=models.CharField(choices=[('Active', 'Active'), ('Non active', 'Non active'), ('Banned', 'Banned')], default='Active', max_length=50),
        ),
    ]
