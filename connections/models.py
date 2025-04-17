from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.models import Notification

User = get_user_model()

class Connection(models.Model):
    sender = models.ForeignKey(User, related_name='sent_connections', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_connections', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sender', 'receiver']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

@receiver(post_save, sender=Connection)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Create notification for new connection request
        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.sender,
            notification_type='connection_request',
            connection=instance
        )
    elif instance.status == 'accepted':
        # Create notification for accepted connection
        Notification.objects.create(
            recipient=instance.sender,
            sender=instance.receiver,
            notification_type='connection_accepted',
            connection=instance
        )
