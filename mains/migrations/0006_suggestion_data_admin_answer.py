# Generated by Django 4.1.5 on 2023-05-31 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mains', '0005_alter_suggestion_data_entry_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion_data',
            name='Admin_answer',
            field=models.TextField(default=None, max_length=350, null=True),
        ),
    ]