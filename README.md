
# cookiecutter-cloudron

_**Note**: This project is a Work In Progress, and is not yet ready for production use._

A cookiecutter template for creating [Django](https://www.djangoproject.com/) applications that run seamlessly on [Cloudron](https://cloudron.io/) and can be developed locally with Docker Compose.

## Features

- **Ready for Cloudron**
- **Ready for Local Development**
- **Modern Django Setup**: 
  - Django 5.1+ with a custom user model
  - PostgreSQL or MySQL database support
  - ASGI support with Granian server
  - Django Ninja API framework
  - HTMX integration
  - Bootstrap 5 frontend
  - Django Debug Toolbar
- **Authentication**:
  - Email-based authentication with django-allauth
  - Multi-factor authentication support
  - Optional Cloudron authentication integration
- **Optional Features**:
  - Redis cache and session storage
  - Celery for background tasks with scheduler
  - S3-compatible storage support

## Requirements

- [Cookiecutter](https://cookiecutter.readthedocs.io/en/latest/installation.html) (`pip install cookiecutter`)
- [Docker](https://docs.docker.com/get-docker/) (which includes Docker Compose) for local development
- [Cloudron CLI](https://docs.cloudron.io/command-line/) (for deployment)
- A Cloudron server with [Cloudron Build Service](https://docs.cloudron.io/apps/build-service/) and [Docker Registry](https://docs.cloudron.io/apps/docker-registry/) installed

## Creating a New Project

```bash
cookiecutter gh:OmenApps/cookiecutter-cloudron
```

You will be prompted for several values:

- `project_name`: The human-readable name of your project
- `project_slug`: The machine-readable name (used for Python packages and file paths)
- `description`: A short description of your project
- `author_name`: Your name
- `author_email`: Your email address
- `version`: Initial version (default: 0.1.0)
- `location`: The domain where your app will be deployed (e.g., `myapp.mydomain.com`)
- `database`: Database choice (postgresql or mysql)
- `use_redis`: Whether to use Redis for caching (yes or no)
- `use_scheduler`: Whether to use Celery for background tasks (yes or no)
- `use_s3_storage`: Whether to use S3-compatible storage (yes or no)
- `use_cloudron_auth`: Whether to use Cloudron's authentication (yes or no)
- `use_sendmail`: Whether to use Cloudron's sendmail (yes or no)
- `asgi_workers`: Number of ASGI workers (default: 2)
- `asgi_threads`: Number of ASGI threads (default: 2)
- `blocking_threads`: Number of blocking threads (default: 2)
- `memory_limit`: Memory limit in Bytes (default: 1000000000 [approx 1 GB])
- `configure_path`: Path for configuration (default: /admin/)

## Local Development

The generated project includes a Docker Compose configuration for local development:

1. Navigate to your project directory:
   ```bash
   cd your_project_name
   ```

2. Build and start the development server:
   ```bash
   docker-compose up -d --build
   ```

3. Create and run migrations:
   ```bash
   docker compose exec web python manage.py makemigrations
   docker compose exec web python manage.py migrate
   ```

4. Create a superuser for local development:
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

5. Access your application at http://localhost:8000

## Building and Deploying to Cloudron

### Prerequisites

1. Install and configure a private [Docker Registry](https://docs.cloudron.io/apps/docker-registry/) on Cloudron (e.g., `hub.mydomain.com`):
   - Install the Docker Registry app on your Cloudron server
   - Configure registry credentials in Cloudron settings

2. Install the [Cloudron Build Service](https://docs.cloudron.io/apps/build-service/):
   - Install the Build Service app on your Cloudron server (e.g., `cbs.mydomain.com`)
   - Be sure to configure service credentials in `/app/data/docker.json` via the File Manager:
   ```json
   {
     "cbs.mydomain.com": {
       "username": "MY_CLOUDRON_USERNAME",
       "password": "MY_CLOUDRON_PASSWORD"
     }
   }
   ```
   - Restart the app after configuration

3. Install the Cloudron CLI and login to your server:
   ```bash
   sudo npm install -g cloudron

   # Assuming you have a Cloudron server at my.mydomain.com
   cloudron login my.mydomain.com
   ```

### Deployment Steps

1. Set the repository for your application:
   ```bash
   cloudron build --set-repository hub.mydomain.com/repositoryname/net.mydomain.appname
   ```

2. Build the application image using the Cloudron Build Service:
   ```bash
   cloudron build --url 'https://cbs.mydomain.com' --build-service-token YOUR_TOKEN
   ```

3. Install the application on Cloudron (replace `myapp.mydomain.com` with your app's location):
   ```bash
   cloudron install -l myapp.mydomain.com --image hub.mydomain.com/repositoryname/net.mydomain.appname:TAG
   ```
   Replace `TAG` with the tag generated in the previous step's output (e.g., `20250223-213319-7599bf78a`).

4. For subsequent updates, use:
   ```bash
   cloudron update -l cloudtest.mydomain.com --image hub.mydomain.com/repositoryname/net.mydomain.appname:NEW_TAG
   ```

## Project Structure

The generated project follows a standard Django structure with some additional files for Cloudron compatibility:

```
your_project_name/
├── your_project_name/         # Main Django project
│   ├── api/                  # Django Ninja API
│   ├── common/               # Common utilities and views
│   ├── templates/            # HTML templates
│   ├── users/                # Custom user model and views
│   ├── asgi.py               # ASGI configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL configuration
│   └── wsgi.py               # WSGI configuration
├── compose/                  # Docker Compose configuration
├── supervisor/               # Supervisor configuration
├── CloudronManifest.json     # Cloudron app manifest
├── Dockerfile                # Docker configuration
├── manage.py                 # Django management script
└── pyproject.toml            # Python project configuration
```

## Backup and Restore

The application includes management commands for backup:

- `backup_db`: Backup the database
- `backup_media`: Backup media files
- `backup_cloudron`: Create a full Cloudron backup

To execute backups:

```bash
python manage.py backup_db
python manage.py backup_media
python manage.py backup_cloudron --api-token YOUR_CLOUDRON_API_TOKEN
```

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
