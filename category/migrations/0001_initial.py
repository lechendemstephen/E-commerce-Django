# Generated by Django 4.2.11 on 2024-05-25 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category_name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(max_length=500, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('cat_image', models.ImageField(blank=True, upload_to='photos/categories')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
    ]