from googleapiclient.http import MediaIoBaseDownload
import io


def get_epw_file_from_drive(service, file_id):
  request = service.files().get_media(fileId=file_id)
  fh = io.BytesIO()
  downloader = MediaIoBaseDownload(fh, request)
  done = False
  while not done:
    _, done = downloader.next_chunk()
  fh.seek(0)
  return fh


def search_file_by_name(service, file_name, folder_id):
  query = f"name='{file_name}' and trashed=false and '{folder_id}' in parents"
  results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
  items = results.get('files', [])

  if not items:
    return None
  else:
    return items[0]['id']