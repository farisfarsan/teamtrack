from django.db import models
from accounts.models import User

class Task(models.Model):
    STATUS = [("PENDING","Pending"),("IN_PROGRESS","In Progress"),
              ("REVIEW","Review"),("COMPLETED","Completed"),("BLOCKED","Blocked")]
    PRIORITY = [("LOW","Low"),("MEDIUM","Medium"),("HIGH","High")]
    TEAMS = (
        ("PROJECT_MANAGER", "Project Manager"),
        ("DESIGN", "Design"),
        ("TECH", "Tech"),
        ("PRODUCT_MANAGEMENT", "Product Management"),
        ("MARKETING", "Marketing")
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name="tasks")
    assigned_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="assigned_tasks")
    team = models.CharField(max_length=20, choices=TEAMS, default="TECH", help_text="Team this task belongs to")
    status = models.CharField(max_length=20,choices=STATUS,default="PENDING")
    priority = models.CharField(max_length=20,choices=PRIORITY,default="MEDIUM")
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self): return self.title

class TaskComment(models.Model):
    COMMENT_TYPES = [
        ("PROGRESS", "Progress Update"),
        ("QUESTION", "Question"),
        ("BLOCKER", "Blocker"),
        ("COMPLETION", "Completion Note"),
        ("GENERAL", "General Comment")
    ]
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES, default="GENERAL")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.name} - {self.get_comment_type_display()}"
