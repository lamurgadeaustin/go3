# Generated by Django 3.0.7 on 2021-03-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("band", "0003_auto_20200911_2108"),
    ]

    operations = [
        migrations.AddField(
            model_name="band",
            name="pub_cal_feed_dirty",
            field=models.BooleanField(default=True),
        ),
    ]
