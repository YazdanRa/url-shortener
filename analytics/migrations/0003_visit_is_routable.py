# Generated by Django 3.0.6 on 2020-05-14 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_visit_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='is_routable',
            field=models.BooleanField(null=True),
        ),
    ]
