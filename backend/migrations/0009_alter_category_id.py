# Generated by Django 5.1.1 on 2025-04-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_temporaryarticle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
