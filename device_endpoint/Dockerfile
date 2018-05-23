FROM alpine:latest
RUN apk add --no-cache python3
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt
COPY . /tmp/src
RUN cd /tmp/src && \
    python3 setup.py install && \
    rm -rf /tmp/src
EXPOSE 8080
ENTRYPOINT ["/usr/bin/run-device_endpoint"]
