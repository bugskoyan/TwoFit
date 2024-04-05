# Generated by Django 5.0.3 on 2024-04-04 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fit', '0004_alter_schedule_day_of_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fitnesstrainer',
            name='gyms',
        ),
        migrations.AlterField(
            model_name='fitnesstrainer',
            name='profile_image',
            field=models.ImageField(blank=True, default='default_profile.jpg', null=True, upload_to='profile_images/', verbose_name='фото профиля'),
        ),
        migrations.AddField(
            model_name='fitnesstrainer',
            name='gyms',
            field=models.ManyToManyField(related_name='trainers', to='fit.gym', verbose_name='спортзалы'),
        ),
    ]
