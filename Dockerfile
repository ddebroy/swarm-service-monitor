FROM python:2.7-alpine3.8

RUN apk add --update bash ca-certificates jq groff less py-pip gcc docker musl-dev\
    && pip install docker \
    && pip install maya \
    && apk --purge -v del py-pip \
    && rm -rf /var/cache/apk/*

COPY monitor.py /monitor.py

RUN chmod 755 /monitor.py

ENTRYPOINT ["/monitor.py"]
