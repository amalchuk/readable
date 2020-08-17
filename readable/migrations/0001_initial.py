import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import readable.models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL)
    ]

    operations = [
        migrations.CreateModel(
            name="Documents",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name="UUID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True, verbose_name="Updated at")),
                ("filename", models.FileField(upload_to=readable.models.documents_upload_directory, verbose_name="Document")),
                ("realname", models.CharField(blank=True, max_length=255, null=True, verbose_name="Real name")),
                ("status", models.IntegerField(choices=[(0, "Failed"), (1, "Created"), (2, "In progress"), (3, "Finished")], default=1, verbose_name="Status"))
            ],
            options={
                "verbose_name": "Document",
                "verbose_name_plural": "Documents",
                "ordering": ["-created_at", "-updated_at"]
            }
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name="UUID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True, verbose_name="Updated at")),
                ("user_agent", models.CharField(blank=True, max_length=255, null=True, verbose_name="User agent")),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name="IP address")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="staff", to=settings.AUTH_USER_MODEL, verbose_name="User"))
            ],
            options={
                "verbose_name": "User's additional information",
                "verbose_name_plural": "Users' additional information",
                "ordering": ["-created_at", "-updated_at"]
            }
        ),
        migrations.CreateModel(
            name="Metrics",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name="UUID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created at")),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True, verbose_name="Updated at")),
                ("is_russian", models.BooleanField(default=False, verbose_name="Is Russian")),
                ("sentences", models.IntegerField(default=0, verbose_name="Sentences")),
                ("words", models.IntegerField(default=0, verbose_name="Words")),
                ("letters", models.IntegerField(default=0, verbose_name="Letters")),
                ("syllables", models.IntegerField(default=0, verbose_name="Syllables")),
                ("document", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="metrics", to="readable.Documents", verbose_name="Document"))
            ],
            options={
                "verbose_name": "Metric",
                "verbose_name_plural": "Metrics",
                "ordering": ["-created_at", "-updated_at"]
            }
        ),
        migrations.AddField(
            model_name="documents",
            name="uploaded_by",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="documents", to="readable.Staff", verbose_name="Uploaded by")
        )
    ]
