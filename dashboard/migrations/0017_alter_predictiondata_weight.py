# Generated by Django 4.1.1 on 2023-02-07 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_predictiondata_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictiondata',
            name='weight',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
