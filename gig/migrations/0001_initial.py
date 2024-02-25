# Generated by Django 3.0.3 on 2020-02-26 02:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("band", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("details", models.TextField(blank=True, null=True)),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("last_update", models.DateTimeField(auto_now=True)),
                ("date", models.DateTimeField()),
                ("address", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "Unknown"),
                            (1, "Confirmed"),
                            (2, "Cancelled"),
                            (3, "Asking"),
                        ],
                        default=0,
                    ),
                ),
                ("is_private", models.BooleanField(default=False)),
                ("invite_occasionals", models.BooleanField(default=True)),
                ("was_reminded", models.BooleanField(default=False)),
                ("hide_from_calendar", models.BooleanField(default=False)),
                ("default_to_attending", models.BooleanField(default=False)),
                ("trashed_date", models.DateTimeField(blank=True, null=True)),
                ("setlist", models.TextField(blank=True, null=True)),
                ("setdate", models.DateTimeField(blank=True, null=True)),
                ("enddate", models.DateTimeField(blank=True, null=True)),
                ("dress", models.TextField(blank=True, null=True)),
                ("paid", models.TextField(blank=True, null=True)),
                ("postgig", models.TextField(blank=True, null=True)),
                ("rss_description", models.TextField(blank=True, null=True)),
                (
                    "band",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gigs",
                        related_query_name="gigs",
                        to="band.Band",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Plan",
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
                    "status",
                    models.IntegerField(
                        choices=[
                            (0, "No Plan"),
                            (1, "Definite"),
                            (2, "Probable"),
                            (3, "Don't Know"),
                            (4, "Probably Not"),
                            (5, "Can't Do It"),
                            (6, "Not Interested"),
                        ],
                        default=0,
                    ),
                ),
                ("feedback_value", models.IntegerField(blank=True, null=True)),
                ("comment", models.CharField(blank=True, max_length=200, null=True)),
                ("last_update", models.DateTimeField(auto_now=True)),
                ("snooze_until", models.DateTimeField(blank=True, null=True)),
                (
                    "assoc",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plans",
                        to="band.Assoc",
                        verbose_name="assoc",
                    ),
                ),
                (
                    "gig",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plans",
                        to="gig.Gig",
                    ),
                ),
                (
                    "plan_section",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="plansections",
                        to="band.Section",
                        verbose_name="plan_section",
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="sections",
                        to="band.Section",
                        verbose_name="section",
                    ),
                ),
            ],
        ),
    ]
