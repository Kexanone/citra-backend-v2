from django.apps import AppConfig
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from time import time
import logging

logger = logging.getLogger(__name__)

class LobbyConfig(AppConfig):
    name = 'lobby'

    def ready(self):
        '''
        Add background scheduler
        '''
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(delete_timed_out_rooms, 'interval', seconds=settings.MAX_ROOM_UPDATE_TIMEOUT_S)
        self.scheduler.start()

def delete_timed_out_rooms():
    '''
    Deletes timed out rooms
    '''
    from .models import Room
    current_time = time()
    timed_out_rooms = Room.objects.filter(timestamp__lt=current_time - settings.MAX_ROOM_UPDATE_TIMEOUT_S)
    count, _ = timed_out_rooms.delete()

    if count > 0:
        logger.info(f'Deleted {count} timed-out rooms.')
