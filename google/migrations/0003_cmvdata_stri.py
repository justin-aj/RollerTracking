# Generated by Django 4.1.7 on 2023-04-04 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmvdata',
            name='stri',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
