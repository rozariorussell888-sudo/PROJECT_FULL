from django.db import models
from accounts.models import Student
from resources.models import ResourceItem

class ResourceRequest(models.Model):

    CATEGORY_CHOICES = [
        ("books", "Books"),
        ("notes", "Notes"),
        ("equipment", "Equipment"),
        ("previous_questions", "Previous Questions"),
        ("course_materials", "Course Materials"),
    ]


    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="resource_requests"
    )


    title = models.CharField(
        max_length=200
    )


    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )


    course_code = models.CharField(
        max_length=50,
        blank=True
    )


    description = models.TextField()


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.title

class ProductRequest(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

                                
    resource = models.ForeignKey(
        ResourceItem,
        on_delete=models.CASCADE,
        related_name="product_requests"
    )

                                  
    requester = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="sent_product_requests"
    )

    message = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["resource", "requester"],
                name="unique_resource_requester"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.requester.full_name} - "
            f"{self.resource.title} - {self.status}"
        )


class ResourceRequestResponse(models.Model):
    """Each student responds independently to a community resource request."""
    STATUS_CHOICES = [("accepted", "Accepted"), ("rejected", "Rejected")]
    request = models.ForeignKey(
        ResourceRequest, on_delete=models.CASCADE, related_name="responses"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="community_request_responses"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["request", "student"], name="unique_student_community_response"
        )]

    def __str__(self):
        return f"{self.student.full_name}: {self.request.title} ({self.status})"


class WebsiteNotification(models.Model):
    """Personal website notifications for requests and responses."""
    recipient = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="website_notifications")
    actor = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sent_website_notifications")
    title = models.CharField(max_length=220)
    kind = models.CharField(max_length=25, choices=[
        ("community_request", "Community request"),
        ("equipment_request", "Equipment request"),
        ("community_response", "Community response"),
        ("equipment_response", "Equipment response"),
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read", "created_at"]) ]

    def __str__(self):
        return f"{self.recipient_id}: {self.title}"

    def destination(self):
        if self.kind in ("community_response", "equipment_response"):
            return "my_requests"
        return "received_requests"
