# Generated by Django 5.1.7 on 2025-03-25 14:01

import django.db.models.deletion
import modelcluster.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retreat', '0007_remove_availableretreat_retreat_page_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retreatpage',
            name='available_retreats',
        ),
        migrations.AlterField(
            model_name='coordinator',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='coordinator',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='RetreatPageAvailableRetreat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_retreat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='retreat.availableretreat')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='retreat_page_available_retreats', to='retreat.retreatpage')),
            ],
        ),
    ]
