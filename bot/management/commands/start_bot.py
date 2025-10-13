from django.core.management.base import BaseCommand
import asyncio
from bot.core import main

class Command(BaseCommand):
    help = 'Запустить Telegram бота'
    
    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Запускаем Telegram бота...')
        )
        asyncio.run(main())