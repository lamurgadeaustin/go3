# Generated by Django 3.1.7 on 2021-03-13 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("member", "0006_remove_member_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
