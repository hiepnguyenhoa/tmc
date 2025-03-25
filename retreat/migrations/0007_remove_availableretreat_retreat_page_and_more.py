# Generated by Django 5.1.7 on 2025-03-25 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retreat', '0006_remove_retreatpage_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availableretreat',
            name='retreat_page',
        ),
        migrations.AddField(
            model_name='retreatpage',
            name='available_retreats',
            field=models.ManyToManyField(blank=True, related_name='retreat_pages', to='retreat.availableretreat'),
        ),
        migrations.AlterField(
            model_name='availableretreat',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='available_retreats', to='retreat.retreatcategory'),
        ),
    ]
