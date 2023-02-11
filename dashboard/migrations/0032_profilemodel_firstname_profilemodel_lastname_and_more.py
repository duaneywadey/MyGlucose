# Generated by Django 4.1.1 on 2023-02-11 02:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0031_profilemodel_address_profilemodel_phonenum_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilemodel',
            name='firstName',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='profilemodel',
            name='lastName',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='profilemodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
