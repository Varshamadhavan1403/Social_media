from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class FriendRequestModel(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')), default='pending')

    def __str__(self):
        return f"From {self.from_user.username} to {self.to_user.username}"

    class Meta:
        unique_together = ('from_user', 'to_user')