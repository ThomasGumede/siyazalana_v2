# Generated by Django 5.1.3 on 2024-06-18 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siyazalana_home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='icon',
            field=models.CharField(default='i', max_length=250),
            preserve_default=False,
        ),
    ]
