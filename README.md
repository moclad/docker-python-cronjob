# docker-python-cronjob
Run a python script to backup a google calendar using a cronjob in docker.
It will send a slack notification in case of success or failure.

## Build Docker
```
docker build -t python-cron .
```
## Run docker container
```
 docker run --env-file .env -it --name calendar-backup --rm -d python-cron
```
## Configuration

```
MINIO_URL= Minio URL
ACCESS_KEY= Minio Access Key
SECRET_KEY= Minio Secret Key
BUCKET_NAME= Bucket where files are going to be stored

BACKUP_DIR=/app/data/
BACKUP_FILE_NAME=calendar-backup
PID_FILE_NAME=backup.pid

CALENDAR=https://calendar.google.com/calendar/ical/xxx%40gmail.com/private-xxxxx/basic.ics #The calendar's download URL

SLACK_HOOK= Slack hook url for notifications.
```

## To get the addresses of your calendar

Go to https://www.google.com/calendar/

Click on the down arrow next to the name of a calendar, in the menu on the left. Select calendar settings in the dropdown menu.

At the bottom, you should have a Private address section, with an ICAL button. Right-click on it, select Copy link address, paste it in the settings.ini, using the formatting above.
If there is no Private address section, you may be using a Google Apps account and then you need to check your organisation's settings.

Note: you can use any http address you like, provided it works with the wget command.

## Slack App Webhook

There are various how-to's showing how to create incomming webhooks in slack. These will guide you to create one and use it python.
