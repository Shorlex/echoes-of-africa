# Generated by Django 5.1 on 2024-09-14 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('heroes', '0007_hero_date_selected_hero_hero_of_the_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hero',
            name='year_of_death',
            field=models.IntegerField(null=True),
        ),
    ]
