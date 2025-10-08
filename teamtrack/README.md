# TeamTrack - Team Task Management System

A comprehensive Django-based task management system designed for teams to collaborate, track progress, and manage projects efficiently.

## 🚀 Features

- **User Management**: Role-based access (Project Managers, Team Members)
- **Task Management**: Create, assign, and track tasks across teams
- **Progress Tracking**: Real-time status updates and progress comments
- **Team Dashboards**: Overview of all team activities
- **Notifications**: Real-time notifications for task updates
- **Meeting Management**: Schedule and manage team meetings

## 👥 Teams Supported

- **Project Manager**: Full administrative access
- **Tech Team**: Development and technical tasks
- **Design Team**: UI/UX and design tasks
- **Product Management**: Product planning and strategy
- **Marketing Team**: Marketing campaigns and content

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Deployment**: Render.com
- **Static Files**: WhiteNoise

## 📋 Quick Start

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd teamtrack
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment

See [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) for detailed deployment instructions to Render.com.

## 🔐 Default Credentials

### Admin User
- **Email**: `admin@example.com`
- **Password**: `admin123`

### Team Members
See the deployment guide for complete user credentials.

## 📁 Project Structure

```
teamtrack/
├── accounts/          # User management
├── tasks/             # Task management
├── meetings/          # Meeting management
├── notifications/     # Notification system
├── dashboard/         # Dashboard views
├── templates/         # HTML templates
├── static/           # Static files
├── teamtrack/        # Django project settings
├── build.sh          # Render build script
├── start.sh          # Render start script
├── render.yaml       # Render configuration
└── requirements.txt  # Python dependencies
```

## 🎯 Key Features

### For Project Managers
- Create and assign tasks to any team member
- View all tasks across all teams
- Edit and delete any task
- Monitor team progress and performance
- Schedule team meetings

### For Team Members
- View assigned tasks
- Update task status (Pending → In Progress → Completed)
- Add progress comments and updates
- View team activities in dashboard
- Receive notifications for updates

## 🔧 Management Commands

- `python manage.py create_users` - Create team member accounts
- `python manage.py clear_sample_data` - Remove sample data
- `python manage.py list_users` - List all users

## 📊 Dashboard Features

- **Admin Dashboard**: Complete system overview with analytics
- **Member Dashboard**: Personal task overview with team visibility
- **Task Analytics**: Progress tracking and completion rates
- **Team Statistics**: Performance metrics per team

## 🚀 Deployment

This project is optimized for deployment on Render.com with:
- PostgreSQL database
- Automatic static file collection
- Production security settings
- Environment variable configuration

## 📞 Support

For deployment issues or questions, refer to the [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md) or check the Render documentation.

## 📄 License

This project is for internal team use. Please ensure proper security measures are in place for production deployment.
