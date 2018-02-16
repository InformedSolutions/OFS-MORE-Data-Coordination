from python:3.5-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir /source
WORKDIR /source
ADD . /source/
RUN pip install -r requirements.txt

ADD crontab /etc/cron.d/deletion
RUN chmod 0644 /etc/cron.d/deletion
Run touch /var/log/cron.log

RUN chmod +x /source/docker-entrypoint.sh
CMD ["/source/docker-entrypoint.sh"]