from django.apps import AppConfig


class MessengerConfig(AppConfig):
    name = 'Messenger'

    def ready(self):
        import Messenger.receivers