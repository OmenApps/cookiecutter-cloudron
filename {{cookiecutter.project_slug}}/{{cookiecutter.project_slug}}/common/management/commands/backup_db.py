"""
Management command to backup database
"""
import os
import datetime
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
{% if cookiecutter.database == "postgresql" %}
import psycopg
{% else %}
import MySQLdb
{% endif %}

class Command(BaseCommand):
    help = 'Create a database backup'

    def handle(self, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = settings.BASE_DIR / 'backups' / 'db'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        {% if cookiecutter.database == "postgresql" %}
        # PostgreSQL backup
        backup_file = backup_dir / f'backup_{timestamp}.sql'
        env = os.environ.copy()
        env['PGPASSWORD'] = settings.DATABASES['default']['PASSWORD']
        
        cmd = [
            'pg_dump',
            '-h', settings.DATABASES['default']['HOST'],
            '-p', settings.DATABASES['default']['PORT'],
            '-U', settings.DATABASES['default']['USER'],
            '-d', settings.DATABASES['default']['NAME'],
            '-F', 'c',  # Custom format
            '-f', str(backup_file)
        ]
        {% else %}
        # MySQL backup
        backup_file = backup_dir / f'backup_{timestamp}.sql'
        cmd = [
            'mysqldump',
            f"--host={settings.DATABASES['default']['HOST']}",
            f"--port={settings.DATABASES['default']['PORT']}",
            f"--user={settings.DATABASES['default']['USER']}",
            f"--password={settings.DATABASES['default']['PASSWORD']}",
            settings.DATABASES['default']['NAME'],
            f"--result-file={backup_file}"
        ]
        {% endif %}

        try:
            subprocess.run(cmd, check=True)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created backup at {backup_file}')
            )

            # If S3 storage is configured, upload to S3
            {% if cookiecutter.use_s3_storage == "yes" %}
            if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                import boto3
                s3 = boto3.client(
                    's3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    region_name=settings.AWS_S3_REGION_NAME
                )
                s3_key = f'backups/db/backup_{timestamp}.sql'
                s3.upload_file(
                    str(backup_file),
                    settings.AWS_STORAGE_BUCKET_NAME,
                    s3_key
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully uploaded backup to S3: {s3_key}')
                )
            {% endif %}

            # Cleanup old backups (keep last 7 days)
            for old_backup in backup_dir.glob('backup_*.sql'):
                if (datetime.datetime.now() - datetime.datetime.fromtimestamp(old_backup.stat().st_mtime)).days > 7:
                    old_backup.unlink()
                    self.stdout.write(
                        self.style.SUCCESS(f'Cleaned up old backup: {old_backup}')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Backup failed: {str(e)}')
            )
            raise