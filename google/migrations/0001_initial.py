# Generated by Django 4.1.7 on 2023-03-29 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CMVData',
            fields=[
                ('id', models.IntegerField(blank=True, primary_key=True, serialize=False)),
                ('cmv', models.IntegerField(blank=True, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]