from django.db import models

# Create your models here.

class FriendRequest(models.Model):

    class RequestChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'

    from_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='to_user')
    request_status = models.CharField(max_length=10, choices=RequestChoices.choices, default=RequestChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'friend_request'
