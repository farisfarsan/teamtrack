from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os

def send_task_assignment_email(task, assigned_to, assigned_by):
    """
    Send email notification when a task is assigned
    """
    try:
        subject = f'New Task Assigned: {task.title}'
        
        # Create email context
        context = {
            'task': task,
            'assigned_to': assigned_to,
            'assigned_by': assigned_by,
            'task_url': f"{settings.BASE_URL}/tasks/{task.pk}/",
            'app_name': 'TeamTrack'
        }
        
        # Render HTML email template
        html_message = render_to_string('emails/task_assignment.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[assigned_to.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_task_update_email(task, updated_by, change_type):
    """
    Send email notification when task status is updated
    """
    try:
        subject = f'Task Updated: {task.title}'
        
        context = {
            'task': task,
            'updated_by': updated_by,
            'change_type': change_type,
            'task_url': f"{settings.BASE_URL}/tasks/{task.pk}/",
            'app_name': 'TeamTrack'
        }
        
        html_message = render_to_string('emails/task_update.html', context)
        plain_message = strip_tags(html_message)
        
        # Send to task assignee and assigner
        recipients = [task.assigned_to.email]
        if task.assigned_by and task.assigned_by.email != task.assigned_to.email:
            recipients.append(task.assigned_by.email)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            html_message=html_message,
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_comment_notification_email(comment, task):
    """
    Send email notification when a comment is added to a task
    """
    try:
        subject = f'New Comment on Task: {task.title}'
        
        context = {
            'comment': comment,
            'task': task,
            'task_url': f"{settings.BASE_URL}/tasks/{task.pk}/",
            'app_name': 'TeamTrack'
        }
        
        html_message = render_to_string('emails/task_comment.html', context)
        plain_message = strip_tags(html_message)
        
        # Send to task assignee and assigner (excluding comment author)
        recipients = []
        if task.assigned_to.email != comment.author.email:
            recipients.append(task.assigned_to.email)
        if task.assigned_by and task.assigned_by.email != comment.author.email and task.assigned_by.email not in recipients:
            recipients.append(task.assigned_by.email)
        
        if recipients:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False,
            )
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
