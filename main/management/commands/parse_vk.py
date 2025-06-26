from django.core.management.base import BaseCommand
from main.vk_parser import parse_vk_posts

class Command(BaseCommand):
    help = 'Parse news from VK group'

    def add_arguments(self, parser):
        parser.add_argument('group_id', type=str, help='VK group ID')

    def handle(self, *args, **options):
        group_id = options['group_id']
        if parse_vk_posts(group_id):
            self.stdout.write(self.style.SUCCESS('Successfully parsed VK posts'))
        else:
            self.stdout.write(self.style.ERROR('Error parsing VK posts'))