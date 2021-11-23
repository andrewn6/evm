FROM ubuntu:16.04

RUN apt-get update && apt-get -y install gcc g++ git curl python-dev

# evm deps
RUN apt-get -y install python3-pip 

# python evm deps
RUN pip3 install -U pip \
    pip3 install -U py-evm
