# Generated by Django 5.1.7 on 2025-04-02 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='retreatcategory',
            options={'ordering': ['-display_order', 'name'], 'verbose_name': 'Retreat Category', 'verbose_name_plural': 'Retreat Categories'},
        ),
        migrations.AlterField(
            model_name='retreatcategory',
            name='display_order',
            field=models.IntegerField(default=0, help_text='Higher numbers appear first in the retreat index page.'),
        ),
        migrations.AlterField(
            model_name='retreatcategory',
            name='name',
            field=models.CharField(help_text='Name of the retreat category', max_length=255, unique=True),
        ),
    ]
