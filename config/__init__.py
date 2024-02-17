from config._secret import *


def get_js_config():
    return {
        'googleClientId': GOOGLE_CLIENT_ID,
        'googleAppId': GOOGLE_APP_ID,
        'azureClientId': AZURE_CLIENT_ID,
    }
