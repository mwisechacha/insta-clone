# Generated by Django 5.0 on 2023-12-28 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpeg', upload_to='profile_pictures'),
        ),
    ]
