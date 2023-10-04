"""
Settings for the Turnitin API plugin.
"""

import os

SECRET_KEY = os.getenv('DJANGO_SECRET', 'open_secret')

# Application definition

INSTALLED_APPS = (
    'statici18n',
    'turnitin_api',
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# statici18n
# https://django-statici18n.readthedocs.io/en/latest/settings.html

STATICI18N_DOMAIN = 'text'
STATICI18N_PACKAGES = (
    'turnitin.translations',
)
STATICI18N_ROOT = 'turnitin/public/js'
STATICI18N_OUTPUT_DIR = 'translations'







def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """

