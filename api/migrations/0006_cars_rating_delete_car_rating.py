# Generated by Django 4.0 on 2021-12-22 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_car_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cars_rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_id', models.IntegerField()),
                ('rating', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Car_rating',
        ),
    ]
