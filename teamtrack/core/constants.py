"""
Shared constants used across the application to avoid duplication.
"""

# Team choices used in User and Task models
TEAMS = (
    ("PROJECT_MANAGER", "Project Manager"),
    ("DESIGN", "Design"),
    ("TECH", "Tech"),
    ("PRODUCT_MANAGEMENT", "Product Management"),
    ("MARKETING", "Marketing")
)

# Task status choices
TASK_STATUS = [
    ("PENDING", "Pending"),
    ("IN_PROGRESS", "In Progress"),
    ("REVIEW", "Review"),
    ("COMPLETED", "Completed"),
    ("BLOCKED", "Blocked")
]

# Task priority choices
TASK_PRIORITY = [
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
    ("HIGH", "High")
]

# Task comment types
TASK_COMMENT_TYPES = [
    ("PROGRESS", "Progress Update"),
    ("QUESTION", "Question"),
    ("BLOCKER", "Blocker"),
    ("COMPLETION", "Completion Note"),
    ("GENERAL", "General Comment")
]

# Pagination settings
ITEMS_PER_PAGE = 10

# File upload paths
TASK_ATTACHMENT_PATH = 'task_attachments/%Y/%m/%d/'
