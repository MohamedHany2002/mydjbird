# Generated by Django 2.2.7 on 2020-01-25 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0012_remove_notification_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
