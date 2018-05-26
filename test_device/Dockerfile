FROM alpine:latest
RUN apk add --no-cache curl
COPY test_device.sh /usr/local/bin
ENTRYPOINT ["/usr/local/bin/test_device.sh"]
