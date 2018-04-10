#!/usr/bin/env python3

from __future__ import print_function

import logging
import os
import sys

from apiclient import discovery
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client as oa2client, tools

logging.basicConfig()
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

SCOPES = [
    'https://www.googleapis.com/auth/drive',
]


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'login':
        del sys.argv[1:2]
        flow = oa2client.flow_from_clientsecrets('client_id.json', SCOPES)
        tools.run_flow(flow, get_store())
        return

    client = get_client()

    upload_filename = sys.argv[1]
    LOG.info('Uploading %s', upload_filename)
    media = MediaFileUpload(upload_filename)

    td_id = get_team_drive(client)['id']
    LOG.info('Team drive id is: %s', td_id)

    files = client.files().list(
        includeTeamDriveItems=True, supportsTeamDrives=True,
        teamDriveId=td_id, corpora='teamDrive',
        q=(
            'mimeType = "application/vnd.google-apps.folder" and '
            'name = "Information Asset Register (229)"'
        )
    ).execute().get('files', [])
    if len(files) != 1:
        LOG.error('cannot find IAR directory')
        sys.exit(1)

    iar_folder = files[0]

    files = client.files().list(
        includeTeamDriveItems=True, supportsTeamDrives=True,
        teamDriveId=td_id, corpora='teamDrive',
        q=(
            'mimeType = "application/vnd.google-apps.folder" and '
            'name = "Export Database" and '
            '"{id}" in parents'.format(id=iar_folder['id'])
        )
    ).execute().get('files', [])
    if len(files) != 1:
        LOG.error('cannot find export directory')
        sys.exit(1)

    export_folder = files[0]

    LOG.info('Found export folder with id: %s', export_folder)

    metadata = {
        'name': os.path.basename(upload_filename),
        'parents': [export_folder['id']]
    }

    LOG.info('Uploading')
    file = client.files().create(
        supportsTeamDrives=True,
        body=metadata, media_body=media, fields='id').execute()
    LOG.info('Uploaded file with id: %s', file['id'])


def get_store():
    store = getattr(get_store, '__store', None)
    if store is not None:
        return store

    setattr(get_store, '__store', file.Storage('./credential-storage.json'))
    return get_store()


def get_client():
    store = get_store()
    if store is None:
        LOG.error('No credentials store, run with login')
        sys.exit(1)
    creds = store.get()
    if not creds or creds.invalid:
        LOG.error('No credentials, run with login')
        sys.exit(1)
    return discovery.build('drive', 'v3', http=creds.authorize(Http()))


def get_team_drive(client):
    LOG.info('Searching for drive')
    team_drives = [
        team_drive for team_drive in
        client.teamdrives().list().execute().get('teamDrives', [])
        if team_drive.get('name') == (
            'Products and Projects - Automation team and UX team')
    ]

    if len(team_drives) == 0:
        LOG.error('Could not find drive')
        raise RuntimeError('Could not find drive')

    return team_drives[0]


if __name__ == '__main__':
    main()
