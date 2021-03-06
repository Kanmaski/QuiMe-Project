# Generated by Django 3.0.6 on 2020-07-18 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=16)),
                ('taker', models.CharField(max_length=100)),
                ('score', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
