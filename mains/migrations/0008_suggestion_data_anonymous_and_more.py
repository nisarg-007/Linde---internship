# Generated by Django 4.1.5 on 2023-06-12 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mains', '0007_rename_answer_suggestion_data_manager_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion_data',
            name='Anonymous',
            field=models.IntegerField(default=None, max_length=1),
        ),
        migrations.AlterField(
            model_name='suggestion_data',
            name='Manager_mail',
            field=models.CharField(max_length=50, null=True),
        ),
    ]