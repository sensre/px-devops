FROM ubuntu:latest
LABEL "about"="This file is created by SenSri for the base docker image"

RUN apt-get -yq update


# Bug "gnuplot: error while loading shared libraries: libQt5Core.so.5: cannot open shared object file: No such file or directory"
# https://askubuntu.com/questions/1041588/virtualbox-not-launching-on-ubuntu-18-04-qt-lib-problem
#RUN apt-get remove -y libqt5core5a && apt-get install -y libqt5core5a