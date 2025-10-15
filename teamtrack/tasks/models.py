from django.db import models
from accounts.models import User
from core.constants import TEAMS, TASK_STATUS, TASK_PRIORITY, TASK_COMMENT_TYPES, TASK_ATTACHMENT_PATH

class Task(models.Model):
    STATUS = TASK_STATUS
    PRIORITY = TASK_PRIORITY
    TEAMS = TEAMS

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="tasks")
    assigned_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name="assigned_tasks")
    team = models.CharField(max_length=20, choices=TEAMS, default="TECH", help_text="Team this task belongs to")
    status = models.CharField(max_length=20,choices=STATUS,default="PENDING")
    priority = models.CharField(max_length=20,choices=PRIORITY,default="MEDIUM")
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self): return self.title

class TaskComment(models.Model):
    COMMENT_TYPES = TASK_COMMENT_TYPES
    
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPES, default="GENERAL")
    message = models.TextField()
    attachment = models.FileField(upload_to=TASK_ATTACHMENT_PATH, blank=True, null=True, help_text="Attach screenshots or files")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.name} - {self.get_comment_type_display()}"
    
    @property
    def has_attachment(self):
        return bool(self.attachment)
    
    @property
    def attachment_name(self):
        if self.attachment:
            return self.attachment.name.split('/')[-1]
        return None
