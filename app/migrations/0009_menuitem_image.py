# Generated by Django 2.2.5 on 2019-10-05 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_menuitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='upload'),
        ),
    ]
