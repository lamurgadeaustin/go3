# Generated by Django 3.0.7 on 2021-03-07 18:59

from django.db import migrations
from django.db import models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("band", "0006_remove_uuid_null"),
    ]

    operations = [
        migrations.AlterField(
            model_name="band",
            name="pub_cal_feed_id",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
