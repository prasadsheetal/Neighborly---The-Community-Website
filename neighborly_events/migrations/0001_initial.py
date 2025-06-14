# Generated by Django 4.2.20 on 2025-05-10 21:01

from django.db import migrations, models
import django.db.models.deletion
import neighborly_events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                ("event_id", models.AutoField(primary_key=True, serialize=False)),
                ("event_name", models.CharField(max_length=255)),
                ("organizer_name", models.CharField(max_length=255)),
                ("organizer_id", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=255)),
                ("date", models.DateField()),
                ("time", models.TimeField()),
                ("visibility", models.CharField(max_length=255)),
                ("tags", models.JSONField(blank=True, default=list)),
                ("recurring", models.BooleanField(default=False)),
                ("max_attendees", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=neighborly_events.models.event_image_upload_path,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventSignUp",
            fields=[
                ("signup_id", models.AutoField(primary_key=True, serialize=False)),
                ("user_id", models.CharField(max_length=255)),
                ("signed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="eventsignup",
                        to="neighborly_events.event",
                    ),
                ),
            ],
        ),
    ]
