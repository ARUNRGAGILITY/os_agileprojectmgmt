# Generated by Django 5.0.3 on 2024-06-16 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_assessment', '0014_assessmentresponse_incorrect_answer_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentscore',
            name='candidate_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assessmentscore',
            name='passing_percentage',
            field=models.IntegerField(default=0),
        ),
    ]
