# Generated by Django 4.1.7 on 2023-09-03 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='currency',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
