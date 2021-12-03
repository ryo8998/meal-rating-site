# Generated by Django 3.2.9 on 2021-11-16 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealRatings', '0003_alter_meal_typicalmealtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='typicalMealTime',
            field=models.CharField(choices=[('Morning', 1), ('Afternoon', 2), ('Evening', 3)], max_length=128),
        ),
    ]