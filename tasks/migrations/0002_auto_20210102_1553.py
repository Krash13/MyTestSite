# Generated by Django 2.2.7 on 2021-01-02 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='executor', to=settings.AUTH_USER_MODEL),
        ),
    ]
