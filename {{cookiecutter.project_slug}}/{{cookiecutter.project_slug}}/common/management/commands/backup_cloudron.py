"""
Management command to create a complete backup via Cloudron API
"""
import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Create a complete backup via Cloudron API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--api-token',
            help='Cloudron API token',
            required=True
        )
        parser.add_argument(
            '--api-server',
            help='Cloudron API server',
            default=os.environ.get('CLOUDRON_API_ORIGIN')
        )

    def handle(self, *args, **options):
        api_token = options['api_token']
        api_server = options['api_server']
        app_id = os.environ.get('CLOUDRON_APP_ID')

        if not api_server:
            self.stdout.write(
                self.style.ERROR('CLOUDRON_API_ORIGIN environment variable not set')
            )
            return

        if not app_id:
            self.stdout.write(
                self.style.ERROR('CLOUDRON_APP_ID environment variable not set')
            )
            return

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_token}'
        }

        try:
            # Create backup
            response = requests.post(
                f'{api_server}/api/v1/apps/{app_id}/backup',
                headers=headers
            )
            response.raise_for_status()

            self.stdout.write(
                self.style.SUCCESS('Successfully initiated Cloudron backup')
            )

            # Get backup status
            backup_id = response.json()['id']
            status_response = requests.get(
                f'{api_server}/api/v1/apps/{app_id}/backups/{backup_id}',
                headers=headers
            )
            status_response.raise_for_status()
            
            self.stdout.write(
                self.style.SUCCESS(f'Backup status: {status_response.json()["state"]}')
            )

        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Backup failed: {str(e)}')
            )
            raise