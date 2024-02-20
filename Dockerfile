FROM python:latest as base-image

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get -y install cron vim wget

FROM base-image

WORKDIR /app

COPY crontab /etc/cron.d/crontab
COPY backup.py /app/backup.py
COPY entry.sh /app/entry.sh
COPY .env /app/.env

RUN printenv > /etc/environment

RUN echo "Europe/Berlin" > /etc/timezone
RUN chmod 0644 /etc/cron.d/crontab
RUN chmod 0777 /app/entry.sh
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
# CMD ["cron", "-f"]
CMD ["/app/entry.sh"]
