"""
Management command to backup media files
"""
import os
import shutil
import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup media files'

    def handle(self, *args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = settings.BASE_DIR / 'backups' / 'media'
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # Create tar archive of media directory
            backup_file = backup_dir / f'media_backup_{timestamp}.tar.gz'
            media_dir = Path(settings.MEDIA_ROOT)
            
            if media_dir.exists():
                shutil.make_archive(
                    str(backup_file)[:-7],  # Remove .tar.gz
                    'gztar',
                    media_dir
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created media backup at {backup_file}')
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
                    s3_key = f'backups/media/media_backup_{timestamp}.tar.gz'
                    s3.upload_file(
                        str(backup_file),
                        settings.AWS_STORAGE_BUCKET_NAME,
                        s3_key
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully uploaded media backup to S3: {s3_key}')
                    )
                {% endif %}

                # Cleanup old backups (keep last 7 days)
                for old_backup in backup_dir.glob('media_backup_*.tar.gz'):
                    if (datetime.datetime.now() - datetime.datetime.fromtimestamp(old_backup.stat().st_mtime)).days > 7:
                        old_backup.unlink()
                        self.stdout.write(
                            self.style.SUCCESS(f'Cleaned up old backup: {old_backup}')
                        )
            else:
                self.stdout.write(
                    self.style.WARNING('Media directory does not exist. Nothing to backup.')
                )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Media backup failed: {str(e)}')
            )
            raise