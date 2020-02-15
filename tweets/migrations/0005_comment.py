# Generated by Django 2.2.7 on 2020-01-24 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0004_auto_20200124_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('tweet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tweets.tweet')),
            ],
        ),
    ]
