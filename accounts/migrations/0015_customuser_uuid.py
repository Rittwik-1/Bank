# Generated by Django 4.0.4 on 2022-09-13 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_customuser_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='uuid',
            field=models.IntegerField(blank=True, default=0),
            preserve_default=False,
        ),
    ]