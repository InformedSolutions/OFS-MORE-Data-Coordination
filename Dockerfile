from python:3.5-slim
ARG PROJECT_SETTINGS

ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN mkdir /source
WORKDIR /source
ADD . /source/
RUN pip install -r requirements.txt

RUN apt-get update -y
RUN apt-get install -y cron
ADD crontab /etc/cron.d/deletion
RUN chmod 0644 /etc/cron.d/deletion
RUN crontab /etc/cron.d/deletion
RUN touch /var/log/cron.log

RUN chmod +x /source/docker-entrypoint.sh
RUN chmod +x /source/cronbash.sh
CMD ["/source/docker-entrypoint.sh"]
