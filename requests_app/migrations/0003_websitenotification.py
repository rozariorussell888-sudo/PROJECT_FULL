from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("requests_app", "0002_resourcerequestresponse"),
    ]

    operations = [
        migrations.CreateModel(
            name="WebsiteNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220)),
                ("kind", models.CharField(choices=[("community_request", "Community request"), ("equipment_request", "Equipment request"), ("community_response", "Community response"), ("equipment_response", "Equipment response")], max_length=25)),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("actor", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sent_website_notifications", to="accounts.student")),
                ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="website_notifications", to="accounts.student")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="websitenotification",
            index=models.Index(fields=["recipient", "is_read", "created_at"], name="requests_ap_recipie_56f8d2_idx"),
        ),
    ]
