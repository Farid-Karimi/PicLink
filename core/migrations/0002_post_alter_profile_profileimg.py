# Generated by Django 4.2.4 on 2023-08-12 15:52

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='profileimg',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
    ]
