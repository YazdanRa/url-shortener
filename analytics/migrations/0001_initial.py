# Generated by Django 3.0.6 on 2020-05-14 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='Title')),
                ('url', models.URLField(verbose_name='URL')),
                ('short_path', models.CharField(max_length=32, unique=True, verbose_name='Short Path')),
                ('description', models.TextField(blank=True, max_length=512, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='short_url', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visited_at', models.DateTimeField(auto_now_add=True)),
                ('is_touch_capable', models.BooleanField()),
                ('is_mobile', models.BooleanField()),
                ('is_tablet', models.BooleanField()),
                ('is_pc', models.BooleanField()),
                ('is_bot', models.BooleanField()),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit', to='analytics.ShortURL')),
            ],
        ),
        migrations.CreateModel(
            name='OperationSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=64)),
                ('url_visited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os', to='analytics.Visit')),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=64)),
                ('brand', models.CharField(max_length=32)),
                ('model', models.CharField(max_length=32)),
                ('url_visited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device', to='analytics.Visit')),
            ],
        ),
        migrations.CreateModel(
            name='Browser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.CharField(max_length=64)),
                ('version', models.CharField(max_length=64)),
                ('url_visited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='browser', to='analytics.Visit')),
            ],
        ),
    ]
