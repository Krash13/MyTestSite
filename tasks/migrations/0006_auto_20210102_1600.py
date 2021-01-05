# Generated by Django 2.2.7 on 2021-01-02 13:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20210102_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completed',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='executor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='executor', to=settings.AUTH_USER_MODEL),
        ),
    ]