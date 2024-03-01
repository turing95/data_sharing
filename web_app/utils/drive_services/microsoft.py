import arrow
from msal import ConfidentialClientApplication
import requests
from django.conf import settings
import jwt
from allauth.socialaccount.models import SocialToken
from io import BytesIO


class MicrosoftService:
    def __init__(self, social_account):
        self.social_account = social_account

    def refresh_token(self, token=None):
        try:
            if token is None:
                social_account = self.social_account
                if social_account is None:
                    return None

                token = SocialToken.objects.get(account=social_account)
            if arrow.get(token.expires_at) < arrow.utcnow():
                # Create a Confidential Client Application
                app = ConfidentialClientApplication(
                    settings.AZURE_CLIENT_ID,
                    client_credential=settings.AZURE_CLIENT_SECRET
                )
                result = app.acquire_token_by_refresh_token(
                    refresh_token=token.token_secret,
                    scopes=[
                        "User.Read",  # access to user's account information
                        "Files.Read.All",
                        "Files.ReadWrite.All",  # access to user's files
                        "Sites.Read.All",  # access to user's sites
                        "Sites.ReadWrite.All",  # access to user's sites
                    ],  # Specify the required scopes
                )
                if 'access_token' in result:
                    # Update token details from result
                    token.token = result['access_token']
                    token.expires_at = arrow.utcnow().shift(seconds=result['expires_in']).datetime
                    token.save()  # Update the token in the database

                    return token
                else:
                    token.delete()
                    return None
            return token
        except SocialToken.DoesNotExist:
            # Handle the case where the user does not have a Microsoft social account
            # or the token does not exist
            return None

    def get_folders(self, folder_name=None, sharepoint_site=None):
        token = self.refresh_token()
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        if sharepoint_site:
            url = f"https://graph.microsoft.com/v1.0/sites/{sharepoint_site}/drive/root/"
        else:
            url = "https://graph.microsoft.com/v1.0/me/drive/root/"
        if folder_name:
            url += f"search(q='{folder_name}')/"
        else:
            url += 'children'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(response.json())
            folders = [item for item in response.json().get('value', []) if 'folder' in item]
            return folders
        else:
            return None  # or handle the error as required

    def get_sites(self):
        token = self.refresh_token()
        url = "https://graph.microsoft.com/v1.0/sites?search=*"
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json().get('value', [])

    @property
    def decoded_token(self):
        token = self.refresh_token()
        rs = jwt.decode(token.token, options={"verify_signature": False})
        return rs

    def is_file_alive(self, file_id, site_id=None):
        token = self.refresh_token()
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        if site_id:
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}"
        else:
            url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
        response = requests.get(url, headers=headers)
        return response.status_code == 200

    def get_file_name(self, file_id, site_id=None):
        token = self.refresh_token()
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        if site_id:
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}"
        else:
            url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('name')
        else:
            return None

    def get_file_url(self, file_id, site_id=None):
        token = self.refresh_token()
        headers = {
            'Authorization': f'Bearer {token.token}'
        }
        if site_id:
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file_id}"
        else:
            url = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('webUrl')  # The URL of the folder
        else:
            return None

    def upload_file(self, file, file_name, folder_id, site_id=None):
        token = self.refresh_token()

        # Set up headers for the request
        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': file.content_type,  # Assuming 'file' is a Django UploadedFile object
        }

        # Prepare the file stream
        file_stream = BytesIO(file.read())
        file_stream.seek(0)

        if site_id:
            url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}:/{file_name}:/content"
        else:
            url = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}:/{file_name}:/content"

        # Send the request to upload the file
        response = requests.put(url, headers=headers, data=file_stream)

        # Check if the upload was successful
        if response.status_code in [200, 201]:
            # return response.json().get('webUrl', None)  # Returns the URL of the uploaded file
            return response.json()  # Returns the ID of the uploaded file
        else:
            # Handle any errors that occur during the upload
            raise Exception(f"Failed to upload file: {response.json()}")

    '''def _get_folders(self, folder_name=None,microsoft_site=None):
        THIS MIGHT BE USEFUL IN THE FUTURE, BUT ATM SEARCH FROM MSFT DOES NOT SEEM TO WORK THE WAY IT SHOULD
        token = self.refresh_token()

        headers = {
            'Authorization': f'Bearer {token.token}',
            'Content-Type': 'application/json'
        }
        # The URL for the Microsoft Graph API search endpoint
        url = 'https://graph.microsoft.com/beta/search/query'

        # The body of the request specifying the search query and entity types
        body = {
            "requests": [
                {
                    "entityTypes": ["driveItem"],
                    "query": {
                        "queryString": folder_name
                    },
                    "from": 0,
                    "size": 25
                }
            ]
        }

        # Send the POST request
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            results = response.json().get('value', [])
            folders = []
            for result in results:  # Loop through each result in the response
                # Each result may contain multiple hits, so we need to examine each one.
                for hit in result.get('hitsContainers', []):
                    # Each hit contains a resource which could be the item we are interested in.
                    for item in hit.get('hits', []):
                        # Now we examine the resource (item) to see if it is a folder.
                        # This assumes 'folder' information is part of the item's resourceData.
                        # Adjust the condition based on the actual structure of your items.
                        resource = item.get('resource', {})
                        folders.append(resource)
            return folders
        else:
            return self.search_personal_drive(folder_name)  # or handle the error as required'''
