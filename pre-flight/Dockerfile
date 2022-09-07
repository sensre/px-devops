FROM ubuntu:latest
#FROM scratch
LABEL "about"="This file is created by SenSri for the base docker image"
RUN apt-get -y update && apt-get install -y build-essential
RUN apt-get install -yq wget curl fio sed  

ADD scripts /opt/pwx/bin/
RUN chmod +x /opt/pwx/bin/*

ENTRYPOINT [/opt/pwx/bin/run-pre-flight]
