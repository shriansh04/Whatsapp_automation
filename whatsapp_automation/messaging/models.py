from django.db import models

class Message(models.Model):
    to = models.CharField(max_length=15)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message to {self.to} at {self.sent_at}"