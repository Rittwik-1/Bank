# Generated by Django 4.0.4 on 2022-09-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_customuser_credit_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='credit_card',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
