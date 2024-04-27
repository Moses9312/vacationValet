from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'hrApp'

    def ready(self):
        import hrApp.signals
