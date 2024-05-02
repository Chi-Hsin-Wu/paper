FROM continuumio/miniconda3:23.10.0-1

RUN mkdir -p /opt/route/
RUN apt-get update && apt-get install -y \
    git \
    vim \
    g++ 

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install ricxappframe==3.2.2 influxdb

ARG RMRVERSION=4.9.0
RUN wget --content-disposition https://packagecloud.io/o-ran-sc/release/packages/debian/stretch/rmr_${RMRVERSION}_amd64.deb/download.deb && dpkg -i rmr_${RMRVERSION}_amd64.deb
RUN wget --content-disposition https://packagecloud.io/o-ran-sc/release/packages/debian/stretch/rmr-dev_${RMRVERSION}_amd64.deb/download.deb && dpkg -i rmr-dev_${RMRVERSION}_amd64.deb
RUN rm -f rmr_${RMRVERSION}_amd64.deb rmr-dev_${RMRVERSION}_amd64.deb
    
ENV LD_LIBRARY_PATH /usr/local/lib/:/usr/local/lib64


COPY src/ /src

