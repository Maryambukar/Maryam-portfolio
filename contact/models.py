from django.db import models


class ContactMessage(models.Model):
    """
    A record of every message submitted, kept in the DB as a backup even
    though the message is also emailed directly — useful if an email ever
    fails to send.
    """
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.subject} — from {self.name}"
