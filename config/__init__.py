from config._secret import *


# TODO REMOVE - PICKER LEGACY
def get_js_config():
    return {
        'googleApiKey': GOOGLE_API_KEY,
        'googleClientId': GOOGLE_CLIENT_ID,
        'googleAppId': GOOGLE_APP_ID,
        'azureClientId': AZURE_CLIENT_ID,
    }
