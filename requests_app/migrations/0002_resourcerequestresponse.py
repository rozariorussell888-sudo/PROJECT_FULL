from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("requests_app", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="ResourceRequestResponse",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("accepted", "Accepted"), ("rejected", "Rejected")], max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("request", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="responses", to="requests_app.resourcerequest")),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_request_responses", to="accounts.student")),
            ],
        ),
        migrations.AddConstraint(
            model_name="resourcerequestresponse",
            constraint=models.UniqueConstraint(fields=("request", "student"), name="unique_student_community_response"),
        ),
    ]
