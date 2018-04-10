# IAR database sync

A (very) hacky script to export the IAR database to the UX team shared drive.

## Quickstart

Install the [Google Cloud SDK](https://cloud.google.com/sdk/downloads) and login
via the following command:

```bash
$ gcloud auth login
```

Install dependencies for the script (ideally in a virtualenv):

```bash
$ pip install -r requirements.txt
```

Download a ``client_id.json`` file as outlined, for example, in [Google's Drive
SDK
code lab](https://codelabs.developers.google.com/codelabs/gsuite-apis-intro/#5).

Authorise the sync application with Google drive:

> **IMPORTANT:** make sure to log in with your @cam account.

```bash
$ ./sync login
```

Run the migration:

```bash
$ ./iar-export.sh
```

## Credentials

``./sync login`` will store credentials in the file
``credentials-storage.json``. You only need to run the login command once.
