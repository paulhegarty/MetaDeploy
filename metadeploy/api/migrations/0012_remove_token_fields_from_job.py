# Generated by Django 2.1.1 on 2018-09-12 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_category_fk_to_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='token',
        ),
        migrations.RemoveField(
            model_name='job',
            name='token_secret',
        ),
    ]