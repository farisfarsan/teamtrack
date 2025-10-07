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
    def __str__(self): return self.title
