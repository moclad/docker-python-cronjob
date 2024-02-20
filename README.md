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

CALENDAR=https://calendar.google.com/calendar/ical/xxx%40gmail.com/private-xxxxx/basic.ics

SLACK_HOOK= Slack hook url for notifications.
```


