# Generated by Django 3.1.7 on 2021-06-18 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='court',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='booking.court'),
            preserve_default=False,
        ),
    ]
