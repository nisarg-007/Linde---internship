# Generated by Django 4.1.5 on 2023-05-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mains', '0004_alter_suggestion_data_entry_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion_data',
            name='Entry_Time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='suggestion_data',
            name='Title',
            field=models.TextField(default=None, max_length=50),
        ),
    ]
