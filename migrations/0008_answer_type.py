# Generated by Django 4.0.2 on 2022-04-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0007_submission_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='type',
            field=models.CharField(choices=[('bg-success', 'success'), ('bg-danger', 'incorrect'), ('bg-primary', 'common')], default='bg-primary', max_length=50),
        ),
    ]
