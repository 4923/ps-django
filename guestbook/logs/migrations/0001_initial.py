# Generated by Django 4.2.8 on 2023-12-21 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('password', models.CharField(max_length=20)),
                ('contents', models.TextField()),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
