# Generated by Django 2.2 on 2021-02-16 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_vaccine_to_be_taken_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccine',
            name='to_be_taken_age',
            field=models.CharField(choices=[('Birth', 'Birth'), ('6 weeks', '6 weeks'), ('10 weeks', '10 weeks'), ('14 weeks', '14 weeks'), ('6 months', ' 6 months'), ('7 months', '7 months'), ('9 months', '9 months'), ('12 months', '12 months'), ('13 months', '13 months'), ('15 months', '15 months'), ('16-18 months', '16-18 months'), ('18 months', '18 months'), ('4-6 years', '4 - 6 years'), ('9 years', '9 years'), ('9 years 6 months', '9 years 6 months'), ('10 years', '10 years')], default='Birth', max_length=20),
        ),
    ]
