# Generated by Django 5.0 on 2024-07-15 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circlemaker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='coin',
            field=models.IntegerField(default=0),
        ),
    ]
