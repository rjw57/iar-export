#!/usr/bin/env bash
set -xe

this_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${this_dir}"

export EXPORT_FILENAME="export-$(date -I).gz"

export INSTANCE_NAME="iar-backend"  # Cloud SQL instance name, *NOT* database name
export FROM_DATABASE_NAME="iar-backend"  # name of database associated with release
export OBJECT_URI="gs://iar-database-exports/${EXPORT_FILENAME}"
gcloud sql export sql --project information-asset-register --database "${FROM_DATABASE_NAME}" "${INSTANCE_NAME}" "${OBJECT_URI}"

TMP_DIR=$(mktemp -d tmp.workspace.XXXXXXXX)
gsutil cp "${OBJECT_URI}" "${TMP_DIR}/${EXPORT_FILENAME}"
./sync.py "${TMP_DIR}/${EXPORT_FILENAME}"
rm -r "${TMP_DIR}"
