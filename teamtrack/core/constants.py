# Team constants
TEAMS = [
    ('development', 'Development'),
    ('design', 'Design'),
    ('marketing', 'Marketing'),
    ('sales', 'Sales'),
    ('support', 'Support'),
    ('management', 'Management'),
]

# User roles
USER_ROLES = [
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('member', 'Member'),
]

# Task priorities
TASK_PRIORITY = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]

# Task statuses
TASK_STATUS = [
    ('todo', 'To Do'),
    ('in_progress', 'In Progress'),
    ('review', 'Review'),
    ('done', 'Done'),
]

# Task comment types
TASK_COMMENT_TYPES = [
    ('comment', 'Comment'),
    ('update', 'Update'),
    ('note', 'Note'),
]

# Task attachment path
TASK_ATTACHMENT_PATH = 'task_attachments/'

# Pagination
ITEMS_PER_PAGE = 20

# Legacy constants for backward compatibility
TASK_PRIORITIES = TASK_PRIORITY
TASK_STATUSES = TASK_STATUS