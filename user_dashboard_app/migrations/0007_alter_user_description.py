# Generated by Django 4.1.3 on 2023-01-02 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_dashboard_app', '0006_user_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='description',
            field=models.TextField(blank=True, default=None),
        ),
    ]
