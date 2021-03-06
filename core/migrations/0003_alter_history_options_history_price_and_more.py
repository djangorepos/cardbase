# Generated by Django 4.0.6 on 2022-07-13 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_card_cardholder_name_alter_card_series'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={'verbose_name_plural': 'History'},
        ),
        migrations.AddField(
            model_name='history',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='number',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
