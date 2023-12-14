# Generated by Django 5.0 on 2023-12-14 07:23

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('caption', models.CharField(max_length=1000)),
                ('posted_at', models.DateTimeField(auto_now_add=True)),
                ('likes', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['posted_at'],
            },
        ),
    ]
