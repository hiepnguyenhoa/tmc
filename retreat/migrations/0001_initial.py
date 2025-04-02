# Generated by Django 5.1.7 on 2025-04-01 20:48

import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetreatIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RetreatPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('zoom_link', models.URLField(blank=True, null=True)),
                ('zoom_room_id', models.CharField(blank=True, max_length=255, null=True)),
                ('zoom_room_password', models.CharField(blank=True, max_length=255, null=True)),
                ('intro', wagtail.fields.RichTextField(blank=True)),
                ('teacher_biography', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='base.teacherbiography')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RetreatDuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('category', models.CharField(help_text='Category of the retreat (e.g., 7-Day Retreat)', max_length=255)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='retreat_durations', to='retreat.retreatpage')),
            ],
        ),
        migrations.CreateModel(
            name='RetreatPageCoordinator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coordinator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='base.coordinator')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordinators', to='retreat.retreatpage')),
            ],
        ),
    ]
