# Generated by Django 4.1.5 on 2023-06-12 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mains', '0011_alter_suggestion_data_anonymous'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestion_data',
            name='Anonymous',
            field=models.IntegerField(default=None, max_length=1),
        ),
    ]
