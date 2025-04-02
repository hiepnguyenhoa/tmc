# Generated by Django 5.1.7 on 2025-04-02 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_retreatcategory_options_and_more'),
        ('retreat', '0002_retreatcategory_alter_retreatduration_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retreatduration',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Category of the retreat (e.g., 7-Day Retreat)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='retreat_durations', to='base.retreatcategory'),
        ),
        migrations.DeleteModel(
            name='RetreatCategory',
        ),
    ]
