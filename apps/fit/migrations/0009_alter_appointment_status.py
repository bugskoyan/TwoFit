# Generated by Django 5.0.3 on 2024-04-05 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0008_alter_fitnesstrainer_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'В ожидании'), ('confirmed', 'Принято'), ('cancelled', 'Отменено')], default='pending', max_length=10, verbose_name='статус'),
        ),
    ]
