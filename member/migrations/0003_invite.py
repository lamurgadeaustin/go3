# Generated by Django 3.0 on 2020-04-01 06:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("band", "0002_assoc_member"),
        ("member", "0002_member_cal_feed_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invite",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="email address"),
                ),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("de", "German"),
                            ("en-us", "English (US)"),
                            ("en-uk", "English (UK)"),
                            ("fr", "French"),
                            ("it", "Italian"),
                        ],
                        default="en",
                        max_length=200,
                    ),
                ),
                (
                    "band",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invites",
                        to="band.Band",
                    ),
                ),
            ],
        ),
    ]
