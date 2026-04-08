import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import logging

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def upload_batch(file_paths, folder_name="IT2012_Processed_Images"):
    service = authenticate_drive()

    # Create folder
    folder_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
    folder = service.files().create(body=folder_metadata, fields='id').execute()
    folder_id = folder.get('id')
    logging.info(f"Created Google Drive folder ID: {folder_id}")

    uploaded_urls = []
    for file_path in file_paths:
        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        uploaded_urls.append(file.get('webViewLink'))
        logging.info(f"Uploaded {file_path} to Drive.")

    return uploaded_urls    