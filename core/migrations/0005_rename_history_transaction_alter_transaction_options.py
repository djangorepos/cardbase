# Generated by Django 4.0.6 on 2022-07-13 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_history_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='History',
            new_name='Transaction',
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('date',)},
        ),
    ]