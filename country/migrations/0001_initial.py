# Generated by Django 3.0.8 on 2020-08-26 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryId', models.CharField(max_length=3)),
                ('iso2Code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=3)),
                ('regionIso', models.CharField(max_length=3)),
                ('regionValue', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CountryCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryName', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('geonameid', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CountryDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryId', models.CharField(max_length=3)),
                ('capitalCity', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=10)),
                ('latitude', models.CharField(max_length=10)),
            ],
        ),
    ]