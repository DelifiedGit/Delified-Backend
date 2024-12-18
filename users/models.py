from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    institution = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

class MUN(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    venue = models.CharField(max_length=255)
    description = models.TextField()
    registration_fees = models.DecimalField(max_digits=10, decimal_places=2)
    custom_fields = models.JSONField(default=dict)

    def __str__(self):
        return self.event_name

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # 'pending', 'completed', 'failed'

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.amount}"

class Registration(models.Model):
    mun = models.ForeignKey(MUN, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    custom_fields = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mun.event_name}"
    
class Community(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_communities')
    members = models.ManyToManyField(CustomUser, related_name='joined_communities')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.name} in {self.community.name}"
    

class Post(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(CustomUser, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.author.username}'s post in {self.community.name if self.community else 'General Feed'}"

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

