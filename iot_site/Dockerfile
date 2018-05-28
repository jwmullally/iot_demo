FROM alpine:latest
RUN apk add --no-cache python3 && \
    install -m 775 -d /var/lib/iot_site
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
COPY . /tmp/src
RUN cd /tmp/src && \
    python3 ./manage.py makemigrations && \
    python3 setup.py install && \
    rm -rf /tmp/src
EXPOSE 8000
ENTRYPOINT ["/usr/bin/run-iot_site.sh"]
