from .models import WebsiteNotification


def navbar_notifications(request):
    """Counts unread notifications for logged-in Students on every page."""
    student_id = request.session.get("student_id")
    if not student_id:
        return {"navbar_unread_notifications": 0}
    return {
        "navbar_unread_notifications": WebsiteNotification.objects.filter(
            recipient_id=student_id, is_read=False
        ).count()
    }
