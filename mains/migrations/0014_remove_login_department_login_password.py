# Generated by Django 4.1.5 on 2023-06-12 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mains', '0013_alter_suggestion_data_anonymous'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='login',
            name='Department',
        ),
        migrations.AddField(
            model_name='login',
            name='Password',
            field=models.CharField(default=None, max_length=10),
        ),
    ]