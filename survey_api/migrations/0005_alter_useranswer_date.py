# Generated by Django 4.0.3 on 2022-03-17 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_api', '0004_alter_useranswer_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
