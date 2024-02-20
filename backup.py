#!/usr/bin/env python3


from minio import Minio
import time
import sys
from subprocess import call,Popen,PIPE
import os.path
from datetime import datetime
import os
from slack_sdk.webhook import WebhookClient

MINIO_URL = os.environ['MINIO_URL']
BUCKET_NAME = os.environ['BUCKET_NAME']
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

CALENDAR = os.environ['CALENDAR']

BACKUP_DIR = os.environ['BACKUP_DIR']
BACKUP_FILE_NAME = os.environ['BACKUP_FILE_NAME']
PID_FILE_NAME = os.environ['PID_FILE_NAME']

SLACK_HOOK = os.environ['SLACK_HOOK']

hook_client = WebhookClient(SLACK_HOOK)

# date, to timestamp the backups
date = str(datetime.today())
year = str(datetime.today().year)

timestamp = datetime.now().replace(microsecond=0).isoformat()

client = Minio(MINIO_URL,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
)

if not os.path.isdir(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

BACKUP_DIR += "backup-" + year + "/"

if not os.path.isdir(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

destination_filename = "%s-%s.ics"%(BACKUP_FILE_NAME, timestamp)
source_file = BACKUP_DIR + destination_filename

pidfile = BACKUP_DIR + PID_FILE_NAME

# test if pid exists
if os.path.isfile(pidfile):
    print(pidfile + " already exists")
    sys.exit(1)


def getCalendarToFile():
    print("Processing calendar... ", CALENDAR)
    args = ['wget', '-c', '--no-check-certificate', '-o', '/dev/null', '-O', source_file, CALENDAR]
    output = Popen(args, stdout=PIPE)
    time.sleep(20)

    return True

def uploadToMinio():
    print("Upload file to minio")

    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
        print("Created bucket", BUCKET_NAME)

    # Upload the file, renaming it in the process
    client.fput_object(
        BUCKET_NAME, destination_filename, source_file,
    )
    print(
        source_file, "successfully uploaded as object",
        destination_filename, "to bucket", BUCKET_NAME,
    )

    time.sleep(20)

    response = hook_client.send(
    text="Google backup successfully done",
    blocks=[
        {
            "type": "section",
            "text":
                {
                    "type": "mrkdwn",
                    "text": "Google calendar backup successfully done:\n File: *" + destination_filename + "*"
                    }
                }
        ]
    )

    return True


try:
    call(["touch", pidfile])

    getCalendarToFile()
    uploadToMinio()

    call(["rm", pidfile])
    call(["rm", source_file])
except:
    response = hook_client.send(
    text="Google backup successfully done",
    blocks=[
        {
            "type": "section",
            "text":
                {
                    "type": "mrkdwn",
                    "text": "Google calendar backup FAILED"
                    }
                }
        ]
    )


print("done!")
sys.exit(0)