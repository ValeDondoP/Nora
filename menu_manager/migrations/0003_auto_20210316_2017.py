# Generated by Django 3.0.8 on 2021-03-16 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu_manager', '0002_auto_20210316_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesmenuanswer',
            name='comentaries',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='employeesmenuanswer',
            name='employee_name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='employeesmenuanswer',
            name='menu_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='menu_manager.MenuOptions'),
        ),
    ]
