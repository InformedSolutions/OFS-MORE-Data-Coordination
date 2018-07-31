from python:3.5-slim
ARG PROJECT_SETTINGS

ENV PYTHONUNBUFFERED 1
RUN apt-get update -y
RUN apt-get install -y cron

ADD requirements.txt /source/
WORKDIR /source
RUN pip install -r requirements.txt

ADD . /source/

ADD crontab /etc/cron.d/deletion
RUN chmod 0644 /etc/cron.d/deletion
RUN crontab /etc/cron.d/deletion
RUN touch /var/log/cron.log

RUN chmod +x /source/docker-entrypoint.sh
RUN chmod +x /source/cronbash.sh
CMD ["/source/docker-entrypoint.sh"]
