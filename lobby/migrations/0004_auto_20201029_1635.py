# Generated by Django 3.1.2 on 2020-10-29 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0003_auto_20201029_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rates',
            name='data',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='rates',
            name='kill_award',
            field=models.FloatField(blank=True, default='0'),
        ),
        migrations.AlterField(
            model_name='rates',
            name='name',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='rates',
            name='price',
            field=models.FloatField(blank=True, default='0'),
        ),
    ]
