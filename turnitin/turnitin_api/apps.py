from django.apps import AppConfig

class TurnitinApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'turnitin_api'

    plugin_app = {
        'settings_config': {
            'lms.djangoapp': {
                'common': {'relative_path': 'settings.common'},
            },
        },
    }
    def ready(self):
        super().ready()
