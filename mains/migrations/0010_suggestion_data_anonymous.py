# Generated by Django 4.1.5 on 2023-06-12 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mains', '0009_remove_suggestion_data_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion_data',
            name='Anonymous',
            field=models.IntegerField(default=None, max_length=1),
        ),
    ]