# Generated by Django 4.1.2 on 2023-11-26 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_traveldestination'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traveldestination',
            old_name='description',
            new_name='keyword',
        ),
        migrations.AddField(
            model_name='traveldestination',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='traveldestination',
            name='duration',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='traveldestination',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='traveldestination',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]